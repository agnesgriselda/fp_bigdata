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

![arsitektur fp bigdata drawio](https://github.com/user-attachments/assets/75ed4fc5-4047-4d34-9b88-7192259ed428)

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


