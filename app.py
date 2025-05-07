import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Load data POS dari Excel
df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

st.title("📍 Cek 3 POS Terdekat dari Lokasi Kamu")

# Ambil parameter dari URL (kalau ada)
query_params = st.query_params
lat_default = float(query_params.get("lat", 0))
lon_default = float(query_params.get("lon", 0))

# Tampilkan input dengan nilai awal dari query param (atau 0)
lat = st.number_input("Latitude Anda", format="%.6f", value=lat_default)
lon = st.number_input("Longitude Anda", format="%.6f", value=lon_default)

# Jalankan otomatis kalau lat & lon dikirim dari URL
auto_run = lat_default != 0 and lon_default != 0

# Tombol manual atau auto run
if st.button("Cek POS Terdekat") or auto_run:
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    st.subheader("Top 3 POS Terdekat:")
    st.table(top3[["POS Name", "lat", "lon", "distance_km"]])

