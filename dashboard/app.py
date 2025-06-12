import streamlit as st
import pandas as pd
from minio import Minio
import io
import plotly.express as px

# =================================================================================
# BAGIAN 1: KONFIGURASI DAN KONEKSI (Tidak ada perubahan)
# =================================================================================
MINIO_ENDPOINT = "localhost:9000"
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
BUCKET_NAME = "processed-data"
DATA_FILE_KEY = "cleaned_insurance_data.csv"

@st.cache_data
def load_data_from_minio():
    try:
        client = Minio(MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False)
        response = client.get_object(BUCKET_NAME, DATA_FILE_KEY)
        csv_data = response.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_data))
        return df
    except Exception as e:
        st.error(f"Gagal mengambil data dari MinIO: {e}")
        return None
    finally:
        if 'response' in locals() and response:
            response.close()
            response.release_conn()

def reverse_one_hot_encoding(df, prefix):
    encoded_columns = [col for col in df.columns if col.startswith(prefix)]
    if not encoded_columns: return None
    original_series = df[encoded_columns].idxmax(axis=1).apply(lambda x: x.replace(prefix, ''))
    return original_series

# =================================================================================
# BAGIAN 2: STYLING KUSTOM (Disinilah "sihirnya")
# =================================================================================
def apply_custom_style():
    custom_css = """
        <style>
            /* Warna dasar dari UI Prediktor */
            :root {
                --background-color: #1a1a2e;
                --card-color: #16213e;
                --font-color: #e0e0e0;
                --primary-color: #0f3460;
                --accent-color: #537895;
                --highlight-color: #e94560;
            }

            /* Ubah warna background utama dan sidebar */
            .stApp {
                background-color: var(--background-color);
            }
            .st-emotion-cache-16txtl3 {
                 background-color: var(--card-color);
            }

            /* Ubah warna teks */
            h1, h2, h3, h4, h5, h6, .st-emotion-cache-16txtl3, .st-emotion-cache-10trblm {
                color: var(--font-color);
            }
            .stMarkdown, .st-emotion-cache-1y4p8pa {
                color: var(--accent-color);
            }

            /* Styling untuk KPI Metrics */
            .st-emotion-cache-1tpl0xr {
                background-color: var(--card-color);
                border: 1px solid var(--primary-color);
                border-radius: 12px;
                padding: 1rem;
            }

            /* Styling Expander */
            .st-emotion-cache-p5msec {
                border-color: var(--primary-color);
                background-color: var(--card-color);
                border-radius: 12px;
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


# =================================================================================
# BAGIAN 3: MEMBANGUN TAMPILAN DASHBOARD
# =================================================================================

st.set_page_config(page_title="Dashboard Biaya Medis", layout="wide", initial_sidebar_state="expanded")

# Terapkan style kustom kita
apply_custom_style()

# --- Muat dan Proses Data ---
df_raw = load_data_from_minio()

if df_raw is not None:
    df = df_raw.copy()
    
    # Rekayasa balik kolom
    smoker_series = reverse_one_hot_encoding(df, 'smoker_')
    if smoker_series is not None: df['smoker'] = smoker_series
    
    region_series = reverse_one_hot_encoding(df, 'region_')
    if region_series is not None: df['region'] = region_series
    
    # --- Sidebar ---
    st.sidebar.header("Filter Data 📊")
    
    selected_region = st.sidebar.selectbox(
        "Pilih Wilayah:",
        options=['Semua Wilayah'] + sorted(df['region'].unique()) if 'region' in df.columns else ['Semua Wilayah']
    )

    selected_smoker = st.sidebar.selectbox(
        "Pilih Status Perokok:",
        options=['Semua Status'] + sorted(df['smoker'].unique()) if 'smoker' in df.columns else ['Semua Status']
    )

    st.sidebar.divider()
    st.sidebar.info("FP Big Data & Data Lakehouse")

    # Terapkan Filter
    filtered_df = df.copy()
    if selected_region != 'Semua Wilayah':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    if selected_smoker != 'Semua Status':
        filtered_df = filtered_df[filtered_df['smoker'] == selected_smoker]
    
    # --- Halaman Utama ---
    st.title("🏥 Dashboard Analisis Biaya Asuransi Medis")
    
    # Metrik Utama (KPI)
    kpi1, kpi2, kpi3 = st.columns(3)
    avg_charges = filtered_df['charges'].mean()
    avg_age = filtered_df['age'].mean()
    avg_bmi = filtered_df['bmi'].mean()

    kpi1.metric(label="Rata-rata Tagihan Asuransi 💵", value=f"${avg_charges:,.2f}")
    kpi2.metric(label="Rata-rata Usia 🎂", value=f"{avg_age:.1f} tahun")
    kpi3.metric(label="Rata-rata BMI ⚖️", value=f"{avg_bmi:.1f}")
    
    # --- Visualisasi Data ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Biaya Berdasarkan Perokok")
        if 'smoker' in filtered_df.columns:
            fig1 = px.box(filtered_df, x='smoker', y='charges', color='smoker',
                          color_discrete_map={'yes': '#e94560', 'no': '#537895'})
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig1, use_container_width=True)
            
    with col2:
        st.subheader("Hubungan Usia dan Biaya Medis")
        fig2 = px.scatter(filtered_df, x='age', y='charges', color='bmi',
                          color_continuous_scale=px.colors.sequential.Plasma)
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig2, use_container_width=True)

    # --- Tabel Data ---
    with st.expander("Lihat Data Lengkap (setelah difilter)"):
        st.dataframe(filtered_df)

else:
    st.error("Gagal memuat data.")