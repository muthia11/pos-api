import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Load data POS dari Excel
df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

st.title("📍 Cek 3 POS Terdekat dari Lokasi Kamu")

# Ambil lokasi user (manual input, karena browser tidak bisa akses GPS via Streamlit)
lat = st.number_input("Latitude Anda", format="%.6f")
lon = st.number_input("Longitude Anda", format="%.6f")

if st.button("Cek POS Terdekat"):
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    st.subheader("Top 3 POS Terdekat:")
    st.table(top3[["name", "lat", "lon", "distance_km"]])
