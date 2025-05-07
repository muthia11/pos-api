import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Load POS
df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

st.title("📍 Cek 3 POS Terdekat dari Lokasi Kamu")

query_params = st.query_params
lat_default = float(query_params.get("lat", 0))
lon_default = float(query_params.get("lon", 0))

lat = st.number_input("Latitude Anda", format="%.6f", value=lat_default)
lon = st.number_input("Longitude Anda", format="%.6f", value=lon_default)

auto_run = lat_default != 0 and lon_default != 0

if st.button("Cek POS Terdekat") or auto_run:
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    # Tambahkan kolom link Google Maps
    top3["Direction"] = top3.apply(
        lambda row: f"[🧭 Arahkan](https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']})", axis=1
    )

    st.subheader("Top 3 POS Terdekat:")
    st.write(top3[["POS Name", "lat", "lon", "distance_km", "Direction"]].to_markdown(index=False), unsafe_allow_html=True)
