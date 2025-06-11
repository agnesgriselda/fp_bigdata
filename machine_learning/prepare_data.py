import os
import io
import json
import pandas as pd
from minio import Minio
from minio.error import S3Error

# --- Konfigurasi MinIO ---
# Sama seperti konfigurasi di skrip consumer, gunakan environment variables
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
RAW_DATA_BUCKET = 'raw-data'
PROCESSED_DATA_BUCKET = 'processed-data'

def create_minio_client():
    """Membuat dan mengembalikan instance MinIO client."""
    print(f"Connecting to MinIO at {MINIO_ENDPOINT}...")
    try:
        client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        print("Successfully connected to MinIO.")
        return client
    except Exception as e:
        print(f"Failed to connect to MinIO: {e}")
        return None

def main():
    """Fungsi utama untuk menjalankan pipeline ETL."""
    minio_client = create_minio_client()
    if not minio_client:
        return

    # 1. EXTRACT: Baca semua file JSON dari bucket 'raw-data'
    print(f"Listing objects in bucket '{RAW_DATA_BUCKET}'...")
    try:
        objects = minio_client.list_objects(RAW_DATA_BUCKET, recursive=True)
        data_list = []
        for obj in objects:
            print(f"Reading file: {obj.object_name}")
            response = minio_client.get_object(RAW_DATA_BUCKET, obj.object_name)
            data = json.loads(response.read())
            data_list.append(data)
        
        if not data_list:
            print("No data found in 'raw-data' bucket. Exiting.")
            return

        df = pd.DataFrame(data_list)
        print(f"Successfully loaded {len(df)} records into a DataFrame.")

    except S3Error as e:
        print(f"Error reading from MinIO: {e}")
        return

    # 2. TRANSFORM: Bersihkan data dan lakukan feature engineering
    print("Starting data transformation...")
    
    # Tangani nilai yang hilang (jika ada) - untuk dataset ini, kemungkinan tidak ada
    df.dropna(inplace=True)

    # Feature Engineering: One-Hot Encoding untuk data kategorikal
    # Kolom 'sex' dan 'smoker' adalah biner, bisa diubah menjadi 0 dan 1
    df['sex'] = df['sex'].apply(lambda x: 1 if x == 'male' else 0)
    df['smoker'] = df['smoker'].apply(lambda x: 1 if x == 'yes' else 0)

    # One-Hot Encoding untuk kolom 'region'
    df = pd.get_dummies(df, columns=['region'], prefix='region', drop_first=True)
    
    # Mengubah nama kolom agar lebih konsisten (misal: region_northwest -> region_northwest)
    df.columns = df.columns.str.replace(' ', '_').str.lower()

    print("Data transformation complete. Final columns:")
    print(df.columns)

    # 3. LOAD: Simpan DataFrame yang sudah bersih ke bucket 'processed-data'
    # Pastikan bucket tujuan ada
    try:
        found = minio_client.bucket_exists(PROCESSED_DATA_BUCKET)
        if not found:
            minio_client.make_bucket(PROCESSED_DATA_BUCKET)
            print(f"Bucket '{PROCESSED_DATA_BUCKET}' created.")
    except S3Error as e:
        print(f"Error creating bucket: {e}")
        return

    # Konversi DataFrame ke format CSV dalam bentuk byte
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    csv_buffer = io.BytesIO(csv_bytes)
    
    output_filename = 'cleaned_insurance_data.csv'
    print(f"Uploading '{output_filename}' to bucket '{PROCESSED_DATA_BUCKET}'...")

    try:
        minio_client.put_object(
            PROCESSED_DATA_BUCKET,
            output_filename,
            data=csv_buffer,
            length=len(csv_bytes),
            content_type='application/csv'
        )
        print("Successfully uploaded cleaned data to MinIO.")
    except S3Error as e:
        print(f"Error uploading to MinIO: {e}")

if __name__ == "__main__":
    main()