# Final Project : Big Data & Data Lakehouse

## Daftar Anggota

| No | Nama Lengkap                  | NRP         |
|----|-------------------------------|-------------|
| 1  | Aswalia Novitriasari          | 5025231012  |
| 2  | Agnes Zenobia Griselda P      | 5025231034  |
| 3  | Rafika Az Zahra Kusumastuti   | 5025231050  |
| 4  | Nisrina Atiqah Dwiputri R     | 5025231075  |

# Prediksi Biaya Medis dengan Machine Learning

## Deskripsi Masalah

Biaya perawatan kesehatan yang terus meningkat menjadi tantangan serius, baik bagi lembaga asuransi maupun pemerintah. Untuk menekan biaya secara efisien, dibutuhkan pemahaman menyeluruh tentang faktor-faktor yang memengaruhi tingginya tagihan medis. Pendekatan berbasis data dapat digunakan untuk beralih dari strategi reaktif (mengobati setelah sakit) menjadi strategi proaktif dan preventif (mencegah berdasarkan risiko).

Melalui analisis data demografis dan karakteristik individu, model prediksi dapat dibangun untuk mengidentifikasi faktor-faktor utama yang memengaruhi biaya kesehatan. Hal ini dapat mendukung keputusan strategis seperti penetapan premi asuransi atau penargetan intervensi kesehatan masyarakat.

## Tujuan Proyek

Membangun model regresi prediktif menggunakan dataset `insurance.csv` dari Kaggle untuk:

- Memprediksi biaya medis individu.
- Menganalisis kontribusi variabel seperti usia, BMI, jumlah anak, status perokok, dan wilayah tempat tinggal terhadap tagihan medis.
- Menyajikan hasil analisis dalam bentuk dashboard interaktif yang dapat diakses oleh pengambil keputusan.

## Dataset

- **Nama Dataset**: [Medical Cost Personal Datasets](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- **Ukuran**: ~55 KB
- **Format**: CSV (Terstruktur)
- **Usability Score**: 10.0
- **Deskripsi**: Berisi informasi demografi dan karakteristik pribadi individu (usia, jenis kelamin, BMI, status merokok, jumlah anak, wilayah) serta total biaya medis yang ditagihkan.

### Mengapa Dataset Ini Cocok?

- Format sederhana, cocok untuk eksplorasi dan pemodelan awal machine learning.
- Dapat digunakan untuk menganalisis dampak faktor-faktor personal terhadap biaya medis.
- Relevan untuk simulasi sistem penetapan premi asuransi berbasis risiko.

---

##  Arsitektur Solusi (Lakehouse Sederhana)

![arsi fp bigdata drawio](https://github.com/user-attachments/assets/4a06d7df-7d6c-41cd-b8fb-999944c996d4)

Walaupun data yang digunakan bersifat statis, pendekatan **data lakehouse** tetap relevan untuk mengatur, menyimpan, dan menganalisis data dalam skala besar dan fleksibel.

### Komponen:
- **MinIO**: Object storage untuk menyimpan file `insurance.csv` dan hasil olahan model.
- **Python**: Proses ETL, analisis eksploratif, dan pelatihan model regresi (menggunakan Pandas, Scikit-learn).
- **Streamlit**: Dashboard interaktif untuk menampilkan prediksi dan visualisasi.
- **FastAPI (opsional)**: API ringan untuk menyajikan data model ke aplikasi frontend atau dashboard.

### Alur Kerja:
1. **Ingest Data**: Dataset `insurance.csv` diunggah ke MinIO.
2. **Preprocessing**: Data dibersihkan dan dikodekan (encoding variabel kategorikal, scaling, dll).
3. **Modeling**: Model regresi dilatih untuk memprediksi `charges`.
4. **Result Storage**: Output model (prediksi & interpretasi) disimpan kembali di MinIO.
5. **Visualization**: Dashboard Streamlit menampilkan:
   - Faktor-faktor paling memengaruhi biaya.
   - Simulasi perubahan variabel (misalnya: apa yang terjadi jika seseorang berhenti merokok).

### Tumpukan Teknologi (Tech Stack)
| Kategori              | Teknologi                                      |
|-----------------------|------------------------------------------------|
| **Containerization**  | Docker, Docker Compose                         |
| **Data Streaming**    | Apache Kafka                                   |
| **Data Lake Storage** | MinIO                                          |
| **Backend & ML**      | Python                                         |
| **Library Python**    | Pandas, Scikit-learn, Kafka-Python, MinIO      |
| **API Service**       | FastAPI, Uvicorn                               |
| **Dashboard**         | Streamlit                                      |
| **Frontend**          | HTML, CSS, JavaScript                          |

### Struktur Proyek
```
fp-bigdata
├── api_service/
│   └── main.py
├── dashboard/
│   └── app.py
├── data_pipeline/
│   ├── consumer.py
│   └── producer.py
├── data_source/
│   └── insurance.csv
├── frontend_ui/
│   ├── index.html
│   └── script.js
├── machine_learning/
│   ├── prepare_data.py
│   └── train_model.py
├── .gitignore
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

## Langkah Pengerjaan
### Langkah 1: Persiapan Lingkungan Awal (Setup)
1. Buat File requirements.txt
   Buat file baru bernama requirements.txt di direktori utama proyek dan isi dengan semua library Python yang dibutuhkan oleh seluruh tim:
   ```
   kafka-python
   minio
   pandas
   scikit-learn
   streamlit
   fastapi
   uvicorn[standard]
   ```
   Setelah file dibuat, instal semua library dengan menjalankan:
   ```
   pip install -r requirements.txt
   ```
   ![WhatsApp Image 2025-06-10 at 01 02 14_c1644d53](https://github.com/user-attachments/assets/35e88f8f-16c3-45e8-9969-0fc0ebba0300)

2. Buat File docker-compose.yml
   Buat file baru bernama docker-compose.yml. File ini akan menjalankan infrastruktur yang Anda butuhkan (Kafka & MinIO).
   ```
   version: '3.8'

   services:
     zookeeper:
       image: confluentinc/cp-zookeeper:7.3.2
       container_name: zookeeper
       hostname: zookeeper
       ports:
         - "2181:2181"
       environment:
         ZOOKEEPER_CLIENT_PORT: 2181
         ZOOKEEPER_TICK_TIME: 2000

     kafka:
       image: confluentinc/cp-kafka:7.3.2
       container_name: kafka
       hostname: kafka
       ports:
         - "9092:9092"
       depends_on:
         - zookeeper
       environment:
         KAFKA_BROKER_ID: 1
         KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
         KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
         KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:29092,PLAINTEXT_HOST://localhost:9092
         KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
         KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0

     minio:
       image: minio/minio:latest
       container_name: minio
       hostname: minio
       ports:
         # Port untuk API S3
         - "9000:9000"
         # Port untuk Web Console/UI
         - "9001:9001"
       volumes:
         - minio_data:/data
       environment:
         MINIO_ROOT_USER: minioadmin
         MINIO_ROOT_PASSWORD: minioadmin
       command: server /data --console-address ":9001"

   volumes:
     minio_data:
   ```

### Langkah 2:  Menjalankan dan Mengkonfigurasi Infrastruktur
1. Jalankan Layanan Docker
   ```
   docker-compose up -d
   ```
   ![image](https://github.com/user-attachments/assets/4973b148-898a-447e-9af3-1eb7c3455b0e)

2. Konfigurasi MinIO (Data Lake)
   - Buka browser dan akses MinIO Web UI di http://localhost:9001.
   - Login dengan kredensial:
      - Username: minioadmin
      - Password: minioadmin
   - Penting: Buat dua bucket baru melalui UI. Anda akan menggunakan raw-data sebagai tujuan.
      - raw-data
      - processed-data

### Langkah 3: Mengembangkan Pipa Data
1. Lokasi dan Pembuatan File
   ```
   fp_bigdata/
      └── data_pipeline/      
          ├── producer.py    
          └── consumer.py
   ```
3. Kembangkan Producer (data_pipeline/producer.py)
   ```
   import time
   import csv
   import json
   from kafka import KafkaProducer
   import os

   KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
   KAFKA_TOPIC = 'insurance_data_stream'
   CSV_FILE_PATH = 'data_source/insurance.csv'
   SIMULATION_DELAY_SECONDS = 1 # Jeda waktu antar pengiriman pesan

   def create_producer():
       """Membuat dan mengembalikan instance KafkaProducer."""
       print(f"Connecting to Kafka Broker at {KAFKA_BROKER}...")
       try:
           producer = KafkaProducer(
               bootstrap_servers=[KAFKA_BROKER],
               value_serializer=lambda v: json.dumps(v).encode('utf-8'),
               api_version=(0, 10, 2) # Sesuaikan jika versi Kafka berbeda
           )
           print("Successfully connected to Kafka Broker.")
           return producer
       except Exception as e:
           print(f"Failed to connect to Kafka Broker: {e}")
           time.sleep(5)
           return create_producer()

   def publish_data(producer, topic):
       """Membaca data dari CSV dan mengirimkannya ke Kafka."""
       print(f"Reading data from {CSV_FILE_PATH} and publishing to topic '{topic}'...")
    
       with open(CSV_FILE_PATH, mode='r') as file:
           csv_reader = csv.DictReader(file)
        
           for row in csv_reader:
               try:
                   message = {
                       "age": int(row["age"]),
                       "sex": row["sex"],
                       "bmi": float(row["bmi"]),
                       "children": int(row["children"]),
                       "smoker": row["smoker"],
                       "region": row["region"],
                       "charges": float(row["charges"])
                   }
                
                   producer.send(topic, value=message)
                   print(f"Sent: {message}")
                
                   time.sleep(SIMULATION_DELAY_SECONDS)
                
               except (ValueError, KeyError) as e:
                   print(f"Skipping row due to data error: {row}. Error: {e}")
                   continue
    
       producer.flush()
       print("All data has been sent.")

   if __name__ == "__main__":
       kafka_producer = create_producer()
       if kafka_producer:
           publish_data(kafka_producer, KAFKA_TOPIC)
           kafka_producer.close()
           print("Producer has been closed.")
   ```
   
3. Kembangkan Consumer (data_pipeline/consumer.py)
   ```
   import json
   import os
   import time
   from kafka import KafkaConsumer
   from minio import Minio
   from minio.error import S3Error
   import io

   # Konfigurasi Kafka
   KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
   KAFKA_TOPIC = 'insurance_data_stream'

   # Konfigurasi MinIO
   MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
   MINIO_ACCESS_KEY = os.environ.get("MINIO_ROOT_USER", "minioadmin")
   MINIO_SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin")
   MINIO_BUCKET_NAME = 'raw-data'

   def create_kafka_consumer():
       """Membuat dan mengembalikan instance KafkaConsumer."""
       print(f"Connecting to Kafka Broker at {KAFKA_BROKER}...")
       try:
           consumer = KafkaConsumer(
               KAFKA_TOPIC,
               bootstrap_servers=[KAFKA_BROKER],
               auto_offset_reset='earliest', # Mulai baca dari pesan paling awal
               group_id='insurance-consumer-group', # Group ID untuk consumer
               value_deserializer=lambda x: json.loads(x.decode('utf-8')),
               api_version=(0, 10, 2)
           )
           print("Successfully connected to Kafka Broker.")
           return consumer
       except Exception as e:
           print(f"Failed to connect to Kafka: {e}")
           time.sleep(5)
           return create_kafka_consumer()

   def create_minio_client():
       """Membuat dan mengembalikan instance MinIO client."""
       print(f"Connecting to MinIO at {MINIO_ENDPOINT}...")
       try:
           client = Minio(
               MINIO_ENDPOINT,
               access_key=MINIO_ACCESS_KEY,
               secret_key=MINIO_SECRET_KEY,
               secure=False # Set True jika menggunakan HTTPS
           )
           print("Successfully connected to MinIO.")
           return client
       except Exception as e:
           print(f"Failed to connect to MinIO: {e}")
           return None

   def setup_minio_bucket(client, bucket_name):
       """Memastikan bucket di MinIO sudah ada, jika tidak, maka dibuat."""
       try:
           found = client.bucket_exists(bucket_name)
           if not found:
               client.make_bucket(bucket_name)
               print(f"Bucket '{bucket_name}' created.")
           else:
               print(f"Bucket '{bucket_name}' already exists.")
       except S3Error as e:
           print(f"Error checking or creating bucket: {e}")
           return False
       return True

   def consume_and_store_data():
       """Mengkonsumsi data dari Kafka dan menyimpannya ke MinIO."""
       consumer = create_kafka_consumer()
       minio_client = create_minio_client()

       if not consumer or not minio_client:
           print("Could not initialize Kafka Consumer or MinIO Client. Exiting.")
           return

       if not setup_minio_bucket(minio_client, MINIO_BUCKET_NAME):
           print(f"Failed to setup MinIO bucket '{MINIO_BUCKET_NAME}'. Exiting.")
           return

       print(f"Listening for messages on topic '{KAFKA_TOPIC}'...")
       try:
           for message in consumer:
               # message.value sudah dalam format dictionary karena value_deserializer
               data = message.value
               print(f"Received: {data}")

               # Buat nama file unik berdasarkan timestamp
               timestamp_ms = int(time.time() * 1000)
               file_name = f"record_{timestamp_ms}.json"

               # Konversi dictionary ke string JSON
               json_data = json.dumps(data, indent=4).encode('utf-8')
               json_stream = io.BytesIO(json_data)

               # Upload file ke MinIO
               try:
                   minio_client.put_object(
                       MINIO_BUCKET_NAME,
                       file_name,
                       json_stream,
                       len(json_data),
                       content_type='application/json'
                   )
                   print(f"Successfully uploaded {file_name} to bucket '{MINIO_BUCKET_NAME}'")
               except S3Error as e:
                   print(f"Error uploading to MinIO: {e}")

       except KeyboardInterrupt:
           print("Stopping consumer...")
       finally:
           consumer.close()
           print("Consumer has been closed.")

   if __name__ == "__main__":
       consume_and_store_data()
   ```

   ### Langkah 4: Eksekusi dan Validasi
   Jalankan pipeline
      - Di Terminal #1, jalankan Consumer terlebih dahulu. Dia harus siap mendengarkan.
        ```
        python data_pipeline/consumer.py
        ```
        ![WhatsApp Image 2025-06-10 at 01 07 46_fcb0a7bc](https://github.com/user-attachments/assets/799ffb96-b43f-4fec-90fc-3a2c445bd55f)

      - Di Terminal #2, jalankan Producer untuk mulai mengirim data.
        ```
        python data_pipeline/producer.py
        ```
        ![WhatsApp Image 2025-06-10 at 01 07 06_1d5294c6](https://github.com/user-attachments/assets/3a346ee0-d06f-4f81-9b2f-41d03aeb18d1)

---

## Contoh Analisis

- **Apakah perokok memiliki biaya medis lebih tinggi dibanding non-perokok?**
- **Berapa besar pengaruh usia terhadap biaya kesehatan?**
- **Bagaimana distribusi biaya berdasarkan wilayah (region)?**

---

## Ide Ekstensi

- Integrasi data tambahan (misal: data gaya hidup, kondisi kronis).
- Eksperimen dengan algoritma regresi lain: Random Forest, Gradient Boosting.
- Penerapan explainable AI (misalnya SHAP) untuk interpretasi fitur.

---

## Referensi

- Dataset: [https://www.kaggle.com/datasets/mirichoi0218/insurance](https://www.kaggle.com/datasets/mirichoi0218/insurance)
- Scikit-learn: https://scikit-learn.org/
- Streamlit: https://streamlit.io/
- MinIO: https://min.io/


