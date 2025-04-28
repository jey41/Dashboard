import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting tampilan halaman
st.set_page_config(page_title="Dashboard Rekomendasi Tanaman & Pemupukan", layout="wide")

# Header dengan desain yang lebih menarik dan warna custom
st.markdown("""
    <style>
        h1 {
            color: #FF6F61;  /* Ganti dengan warna yang diinginkan */
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 30px;  /* Ukuran font lebih kecil */
        }
        h5 {
            color: #3E4A59;  /* Warna lebih gelap untuk subheader */
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 16px;  /* Ukuran font lebih kecil */
        }
        .header {
            text-align: center;
            font-size: 28px;  /* Ukuran font lebih kecil */
            background-color: #6C67FC;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
        }
    </style>
    <div class="header">
        <h1>🌾 Dashboard Rekomendasi Tanaman & Pemupukan</h1>
        <h5>📊 Analisis Kebutuhan Pupuk dan Rekomendasi Tanaman Berdasarkan Kondisi Tanah</h5>
    </div>
""", unsafe_allow_html=True)

# Sidebar untuk filter dan input
st.sidebar.header("🔧 Opsi Dashboard")

# Filter pilihan data
feature_selected = st.sidebar.selectbox("Pilih Fitur untuk Distribusi:", ['temperature', 'humidity', 'ph', 'Total_NPK'])
scatter_feature = st.sidebar.selectbox("Pilih Fitur untuk Scatter Plot:", ['N', 'P', 'K', 'temperature', 'humidity'])

# Memuat Data
try:
    df = pd.read_csv('crop_recommendation.csv')
except Exception as e:
    st.stop()

# Menampilkan data sample
with st.expander("📂 Klik untuk melihat 5 data pertama") :
    st.dataframe(df.head())

# 1. Distribusi Data Fitur
st.subheader(f"📊 Distribusi {feature_selected}")
fig1, ax1 = plt.subplots(figsize=(6, 4))  # Ukuran lebih kecil
sns.histplot(df[feature_selected], bins=30, kde=True, color='skyblue', ax=ax1)
ax1.set_title(f'Distribusi {feature_selected}', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
st.pyplot(fig1)

# 2. Perbandingan Rata-rata Kebutuhan Pupuk Tiap Unsur Hara
st.subheader("🏭 Perbandingan Rata-rata Kebutuhan Pupuk (N, P, K)")
avg_nutrients = df[['N', 'P', 'K']].mean()
fig2, ax2 = plt.subplots(figsize=(5, 4))  # Ukuran lebih kecil
avg_nutrients.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax2)
ax2.set_ylabel('Kebutuhan Pupuk (kg)', fontsize=8)  # Ukuran font kecil
ax2.set_title('Rata-rata Kebutuhan Pupuk per Unsur Hara', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
ax2.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig2)

# 3. Korelasi antara Pilihan Fitur dengan Total NPK
st.subheader(f"🔗 Korelasi antara {scatter_feature} dan Total NPK")
fig4, ax4 = plt.subplots(figsize=(5, 4))  # Ukuran lebih kecil
sns.scatterplot(x=df[scatter_feature], y=df['Total_NPK'], ax=ax4, color='#ff7f0e')
ax4.set_xlabel(scatter_feature, fontsize=8, color='#5f6368')  # Ukuran font kecil
ax4.set_ylabel('Total NPK (kg)', fontsize=8, color='#5f6368')  # Ukuran font kecil
ax4.set_title(f'Scatter Plot: {scatter_feature} vs Total NPK', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
st.pyplot(fig4)

# 4. Rekomendasi Tanaman Berdasarkan Kategori pH
st.subheader("🌱 Rekomendasi Tanaman Berdasarkan Kategori pH")
ph_mapping = {'Asam': 0, 'Netral': 1, 'Basa': 2}
df['ph_category'] = df['ph_category'].map(ph_mapping)
st.dataframe(df[['ph_category', 'label']].groupby('ph_category')['label'].value_counts())

# Menyaring data berdasarkan kategori pH dan memberikan rekomendasi tanaman
ph_category = st.sidebar.selectbox("Pilih Kategori pH untuk Rekomendasi Tanaman:", ['Asam', 'Netral', 'Basa'])
filtered_data = df[df['ph_category'] == ph_mapping[ph_category]]
st.write(f"Rekomendasi tanaman untuk kategori pH {ph_category}:")
st.dataframe(filtered_data[['label', 'N', 'P', 'K', 'ph_category']].head())

# 5. Menyimpan dan menampilkan model rekomendasi jika diperlukan
# st.subheader("📈 Model Rekomendasi Tanaman")
# Dengan menggunakan model untuk rekomendasi jika diperlukan di masa depan

