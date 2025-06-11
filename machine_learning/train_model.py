import os
import io
import pandas as pd
import pickle
from minio import Minio
from minio.error import S3Error
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# --- Konfigurasi MinIO ---
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ROOT_USER", "minioadmin")
MINIO_SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
PROCESSED_DATA_BUCKET = 'processed-data'
CLEANED_DATA_FILE = 'cleaned_insurance_data.csv'
MODEL_FILE_NAME = 'insurance_model.pkl'

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
    """Fungsi utama untuk menjalankan pipeline training."""
    minio_client = create_minio_client()
    if not minio_client:
        return

    # 1. Muat data yang sudah dibersihkan dari MinIO
    print(f"Downloading '{CLEANED_DATA_FILE}' from bucket '{PROCESSED_DATA_BUCKET}'...")
    try:
        response = minio_client.get_object(PROCESSED_DATA_BUCKET, CLEANED_DATA_FILE)
        # Langsung baca ke pandas DataFrame
        df = pd.read_csv(response)
        print("Successfully loaded data.")
    except S3Error as e:
        print(f"Error downloading data from MinIO: {e}")
        return
    finally:
        response.close()
        response.release_conn()

    # 2. Persiapan Data untuk Model
    print("Preparing data for training...")
    X = df.drop('charges', axis=1)
    y = df['charges']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} testing samples.")

    # 3. Latih Model Machine Learning
    print("Training RandomForestRegressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    print("Model training complete.")

    # 4. Evaluasi Performa Model
    print("Evaluating model performance...")
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    print("--- Model Evaluation ---")
    print(f"R-squared (R²): {r2:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print("------------------------")

    # 5. Simpan Model yang Sudah Terlatih ke MinIO
    print(f"Saving model as '{MODEL_FILE_NAME}'...")
    # Serialisasi model menggunakan pickle
    model_bytes = pickle.dumps(model)
    model_buffer = io.BytesIO(model_bytes)

    try:
        minio_client.put_object(
            PROCESSED_DATA_BUCKET,
            MODEL_FILE_NAME,
            data=model_buffer,
            length=len(model_bytes),
            content_type='application/octet-stream'
        )
        print(f"Successfully uploaded model to bucket '{PROCESSED_DATA_BUCKET}'.")
    except S3Error as e:
        print(f"Error uploading model to MinIO: {e}")

if __name__ == "__main__":
    main()