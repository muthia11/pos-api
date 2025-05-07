import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Theme setup
BFI_BLUE = "#005BAC"
st.set_page_config(page_title="POS Terdekat BFI", page_icon="📍")

# Load data
df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

# Ambil lokasi user dari URL
query_params = st.query_params
lat_default = float(query_params.get("lat", 0))
lon_default = float(query_params.get("lon", 0))

# Header UI
st.markdown(f"<h2 style='color:{BFI_BLUE}'>📍 Cari POS Terdekat BFI</h2>", unsafe_allow_html=True)
lat = st.number_input("Latitude Anda", format="%.6f", value=lat_default)
lon = st.number_input("Longitude Anda", format="%.6f", value=lon_default)
auto_run = lat_default != 0 and lon_default != 0

if st.button("🔎 Cek POS Terdekat") or auto_run:
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    # Tambahkan link Google Maps
    top3["Direction"] = top3.apply(
        lambda row: f"[🧭 Arah ke sini](https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']})",
        axis=1
    )

    # Tampilkan Kartu Informasi
    st.markdown(f"<h4 style='color:{BFI_BLUE}'>Top 3 POS Terdekat:</h4>", unsafe_allow_html=True)
    for i, row in top3.iterrows():
        st.markdown(f"""
        <div style="border:1px solid {BFI_BLUE}; border-radius:10px; padding:16px; margin-bottom:12px;">
            <h5 style="margin-bottom:8px;">📌 {i+1}. {row['POS Name']}</h5>
            <ul>
                <li><b>Latitude:</b> {row['lat']}</li>
                <li><b>Longitude:</b> {row['lon']}</li>
                <li><b>Jarak:</b> {row['distance_km']:.2f} km</li>
                <li>{row['Direction']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Tampilkan Map Interaktif
    st.markdown(f"<h4 style='color:{BFI_BLUE}'>🗺️ Lokasi di Peta</h4>", unsafe_allow_html=True)
    map_center = [lat, lon]
    m = folium.Map(location=map_center, zoom_start=13)

    # Marker lokasi user
    folium.Marker(location=map_center, popup="📍 Lokasi Anda", icon=folium.Icon(color="blue")).add_to(m)

    # Marker POS terdekat
    for _, row in top3.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['POS Name']} ({row['distance_km']:.2f} km)",
            icon=folium.Icon(color="red")
        ).add_to(m)

    st_folium(m, width=700, height=500)
