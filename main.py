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

# 1. Statistik Deskriptif
st.subheader("📊 Statistik Deskriptif")
st.write("Menampilkan statistik deskriptif untuk fitur numerik")
st.dataframe(df.describe())

# 2. Distribusi Data Fitur
st.subheader(f"📊 Distribusi {feature_selected}")
fig1, ax1 = plt.subplots(figsize=(6, 4))  # Ukuran lebih kecil
sns.histplot(df[feature_selected], bins=30, kde=True, color='skyblue', ax=ax1)
ax1.set_title(f'Distribusi {feature_selected}', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
st.pyplot(fig1)

# 3. Korelasi Antar Fitur
st.subheader("🔗 Korelasi Antar Fitur")
correlation = df.corr()  # Menghitung korelasi antar fitur numerik
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
ax2.set_title('Korelasi Antar Fitur', fontsize=10, color='#2d5c8c')
st.pyplot(fig2)

# 4. Deteksi Outlier
st.subheader("📊 Deteksi Outlier")
# Menggunakan boxplot untuk mendeteksi outlier
fig3, ax3 = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df[['N', 'P', 'K', 'temperature', 'humidity', 'rainfall']], ax=ax3)
ax3.set_title("Boxplot - Deteksi Outlier", fontsize=10, color='#2d5c8c')
st.pyplot(fig3)

# 5. Perbandingan Rata-rata Kebutuhan Pupuk Tiap Unsur Hara
st.subheader("🏭 Perbandingan Rata-rata Kebutuhan Pupuk (N, P, K)")
avg_nutrients = df[['N', 'P', 'K']].mean()
fig4, ax4 = plt.subplots(figsize=(5, 4))  # Ukuran lebih kecil
avg_nutrients.plot(kind='bar', color=['#1f77b4', '#ff7f0e', '#2ca02c'], ax=ax4)
ax4.set_ylabel('Kebutuhan Pupuk (kg)', fontsize=8)  # Ukuran font kecil
ax4.set_title('Rata-rata Kebutuhan Pupuk per Unsur Hara', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
ax4.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig4)

# 6. Korelasi antara Pilihan Fitur dengan Total NPK
st.subheader(f"🔗 Korelasi antara {scatter_feature} dan Total NPK")
fig5, ax5 = plt.subplots(figsize=(5, 4))  # Ukuran lebih kecil
sns.scatterplot(x=df[scatter_feature], y=df['Total_NPK'], ax=ax5, color='#ff7f0e')
ax5.set_xlabel(scatter_feature, fontsize=8, color='#5f6368')  # Ukuran font kecil
ax5.set_ylabel('Total NPK (kg)', fontsize=8, color='#5f6368')  # Ukuran font kecil
ax5.set_title(f'Scatter Plot: {scatter_feature} vs Total NPK', fontsize=8, color='#2d5c8c')  # Ukuran font kecil
st.pyplot(fig5)

# 7. Rekomendasi Tanaman Berdasarkan Kategori pH
st.subheader("🌱 Rekomendasi Tanaman Berdasarkan Kategori pH")

# Mapping kategori pH
ph_mapping = {'Asam': 0, 'Netral': 1, 'Basa': 2}
df['ph_category'] = df['ph_category'].map(ph_mapping)

# Menghitung jumlah tanaman untuk masing-masing kategori pH
ph_count = df.groupby('ph_category')['label'].value_counts().unstack(fill_value=0)

# Membuat grafik bar
fig6, ax6 = plt.subplots(figsize=(8, 6))  # Ukuran grafik
ph_count.plot(kind='bar', stacked=True, ax=ax6, color=sns.color_palette("Set3", n_colors=len(ph_count.columns)))
ax6.set_title("Distribusi Tanaman Berdasarkan Kategori pH", fontsize=10, color='#2d5c8c')  # Judul
ax6.set_xlabel("Kategori pH", fontsize=8)
ax6.set_ylabel("Jumlah Tanaman", fontsize=8)
ax6.set_xticklabels(['Asam', 'Netral', 'Basa'], rotation=0)  # Label x-axis
ax6.legend(title="Tanaman", fontsize=8)
ax6.grid(axis='y', linestyle='--', alpha=0.5)
st.pyplot(fig6)

# Menyaring data berdasarkan kategori pH yang dipilih oleh pengguna
ph_category = st.sidebar.selectbox("Pilih Kategori pH untuk Rekomendasi Tanaman:", ['Asam', 'Netral', 'Basa'])

# Filter data berdasarkan kategori pH yang dipilih
filtered_data = df[df['ph_category'] == ph_mapping[ph_category]]

# Menampilkan rekomendasi tanaman untuk kategori pH yang dipilih
st.write(f"Rekomendasi tanaman untuk kategori pH {ph_category}:")
st.dataframe(filtered_data[['label', 'N', 'P', 'K', 'ph_category']].head())
