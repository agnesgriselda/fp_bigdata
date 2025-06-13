import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio

# --- KONFIGURASI ---
app = FastAPI(title="API Prediksi Biaya Medis - Produksi")
MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "processed-data"
MODEL_FILE_KEY = "insurance_model.pkl" # Nama model dari Orang 2
LOCAL_MODEL_PATH = "downloaded_model.pkl" # Nama file sementara di lokal

# --- Middleware CORS (Penting untuk Frontend) ---
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- LOAD MODEL DARI MINIO SAAT STARTUP ---
try:
    client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)
    client.fget_object(BUCKET_NAME, MODEL_FILE_KEY, LOCAL_MODEL_PATH)
    model = joblib.load(LOCAL_MODEL_PATH)
    print("Model 'insurance_model.pkl' berhasil di-load dari MinIO.")
except Exception as e:
    model = None
    print(f"GAGAL me-load model dari MinIO: {e}")

# --- MODEL DATA INPUT ---
class PredictionRequest(BaseModel):
    age: int; sex: str; bmi: float; children: int; smoker: str; region: str

# --- ENDPOINT ---
@app.post("/predict")
def predict_insurance(data: PredictionRequest):
    if model is None: 
        return {"error": "Model tidak tersedia atau gagal di-load."}
    
    # 1. Konversi data input Pydantic ke DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # 2. Lakukan One-Hot Encoding pada input agar sesuai dengan data training
    # Ini adalah langkah krusial!
    input_df = pd.get_dummies(input_df, columns=['sex', 'smoker', 'region'], drop_first=True)
    
    # 3. Pastikan semua kolom yang dibutuhkan model ada di input_df
    # Jika tidak ada, tambahkan dengan nilai 0
    model_features = model.feature_names_in_ # Dapatkan nama fitur dari model yang sudah dilatih
    for feature in model_features:
        if feature not in input_df.columns:
            input_df[feature] = 0
            
    # 4. Urutkan kolom agar sama persis dengan urutan saat training
    input_df = input_df[model_features]

    # 5. Lakukan prediksi
    prediction = model.predict(input_df)
    
    return {"predicted_charges": prediction[0]}