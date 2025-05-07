import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import requests
import folium
from streamlit_folium import st_folium

# Konstanta
BFI_BLUE = "#005BAC"
st.set_page_config(page_title="POS Terdekat BFI", page_icon="📍")

# Load data POS
df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

# Fungsi geocoding alamat -> lat/lon via Nominatim
def get_coordinates_from_address(alamat):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": alamat,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "streamlit-pos-bfi"}
    response = requests.get(url, params=params, headers=headers).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    else:
        return None, None

# Tampilan judul
st.markdown(f"<h2 style='color:{BFI_BLUE}'>📍 Cari POS Terdekat BFI</h2>", unsafe_allow_html=True)

# Input alamat
alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

if alamat_input:
    lat, lon = get_coordinates_from_address(alamat_input)
    if lat and lon:
        user_loc = (lat, lon)
        df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
        top3 = df.sort_values("distance_km").head(3)

        st.markdown(f"<h4 style='color:{BFI_BLUE}'>Top 3 POS Terdekat:</h4>", unsafe_allow_html=True)

        for i, row in top3.iterrows():
            st.markdown(f"""
            <div style="border:1px solid {BFI_BLUE}; border-radius:10px; padding:16px; margin-bottom:12px;">
                <h5 style="margin-bottom:8px;">📌 {i+1}. {row['POS Name']}</h5>
                <p>{row['alamat']}</p>
                <a href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" target="_blank">
                    <button style='background-color:{BFI_BLUE}; color:white; padding:8px 16px; border:none; border-radius:5px;'>🧭 Arahkan</button>
                </a>
            </div>
            """, unsafe_allow_html=True)

        # Map interaktif
        st.markdown(f"<h4 style='color:{BFI_BLUE}'>🗺️ Lokasi di Peta</h4>", unsafe_allow_html=True)
        m = folium.Map(location=user_loc, zoom_start=13)
        folium.Marker(location=user_loc, popup="📍 Lokasi Anda", icon=folium.Icon(color="blue")).add_to(m)

        for _, row in top3.iterrows():
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=row["POS Name"],
                icon=folium.Icon(color="red")
            ).add_to(m)

        st_folium(m, width=700, height=500)

    else:
        st.error("❌ Lokasi tidak ditemukan. Mohon periksa kembali alamat.")
