from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Inisialisasi FastAPI
app = FastAPI(title="Crop Recommendation API")

# Load model dan scaler (ganti path sesuai model yang sudah disimpan)
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Skema input
class SoilData(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

# Fungsi untuk preprocessing input
def preprocess_input(data: SoilData):
    # Buat DataFrame dari input
    df = pd.DataFrame([{
        "N": data.N,
        "P": data.P,
        "K": data.K,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,  # Kolom 'ph' tetap ada di input
        "rainfall": data.rainfall
    }])

    # Fitur tambahan: Total NPK (N + P + K) dan Rasio Unsur Hara
    df["Total_NPK"] = df["N"] + df["P"] + df["K"]
    df["N_to_P_ratio"] = df["N"] / (df["P"] + 1e-5)  # Hindari pembagian dengan nol
    df["N_to_K_ratio"] = df["N"] / (df["K"] + 1e-5)

    # Kategorisasi pH
    def categorize_ph(ph_value):
        if ph_value < 6.5:
            return 'Asam'
        elif 6.5 <= ph_value <= 7.5:
            return 'Netral'
        else:
            return 'Basa'

    df["ph_category"] = df["ph"].apply(categorize_ph)

    # Label Encoding ph_category menjadi angka (0: Asam, 1: Netral, 2: Basa)
    ph_mapping = {'Asam': 0, 'Netral': 1, 'Basa': 2}
    df['ph_category'] = df['ph_category'].map(ph_mapping)

    # Pastikan urutan kolom sesuai dengan yang diharapkan oleh model
    df = df[[ 
        "N", "P", "K", "temperature", "humidity", "ph", "rainfall",
        "Total_NPK", "N_to_P_ratio", "N_to_K_ratio", 
        "ph_category"  # Kolom ph_category tetap ada setelah encoding
    ]]

    # Normalisasi
    df_scaled = scaler.transform(df)
    return df_scaled

@app.get("/")
def read_root():
    return {"message": "Crop Prediction API is running"}

# Endpoint untuk prediksi tanaman
@app.post("/predict")
def predict_crop(data: SoilData):
    processed = preprocess_input(data)
    prediction = model.predict(processed)[0]  # Prediksi dari model
    
    # Menangani prediksi desimal
    prediction = int(round(prediction))  # Pembulatan ke integer

    # Define mapping label sesuai dengan prediksi yang dihasilkan model
    result = {
        0: "rice",  # 0 - Rice
        1: "maize",  # 1 - Maize
        2: "chickpea",  # 2 - Chickpea
        3: "kidneybeans",  # 3 - Kidneybeans
        4: "pigeonpeas",  # 4 - Pigeonpeas
        5: "mothbeans",  # 5 - Mothbeans
        6: "mungbean",  # 6 - Mungbean
        7: "blackgram",  # 7 - Blackgram
        8: "lentil",  # 8 - Lentil
        9: "pomegranate",  # 9 - Pomegranate
        10: "banana",  # 10 - Banana
        11: "mango",  # 11 - Mango
        12: "grapes",  # 12 - Grapes
        13: "watermelon",  # 13 - Watermelon
        14: "muskmelon",  # 14 - Muskmelon
        15: "apple",  # 15 - Apple
        16: "orange",  # 16 - Orange
        17: "papaya",  # 17 - Papaya
        18: "coconut",  # 18 - Coconut
        19: "cotton",  # 19 - Cotton
        20: "jute",  # 20 - Jute
        21: "coffee"  # 21 - Coffee
    }

    # Menangani kasus ketika nilai prediksi tidak ditemukan di result
    predicted_crop = result.get(prediction, "Unknown Crop")  # Jika prediksi tidak ditemukan, default ke "Unknown Crop"
    
    # Log untuk debugging
    print(f"Prediction: {prediction}")
    print(f"Predicted crop: {predicted_crop}")

    return {
        "predicted_crop": predicted_crop,  # Nama tanaman yang diprediksi
        "prediction_value": int(prediction)  # Nilai numerik prediksi
    }
