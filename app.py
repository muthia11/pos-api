import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Konfigurasi dasar
st.set_page_config(page_title="POS Terdekat BFI", layout="centered")

# Background putih di semua mode
st.markdown("""
    <style>
        .stApp {
            background-color: white !important;
        }
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Logo BFI
st.markdown("""
    <div style='text-align:center; margin-bottom: 10px;'>
        <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
    </div>
""", unsafe_allow_html=True)

# Judul
st.markdown("<h2 style='text-align:center; color:#005BAC;'>📍 Cek POS Terdekat</h2>", unsafe_allow_html=True)

# Input alamat
alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

# Query param fallback
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

# Fungsi geocoding
def get_coordinates_from_address(alamat):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": alamat, "format": "json", "limit": 1}
    headers = {"User-Agent": "streamlit-pos-app"}
    response = requests.get(url, params=params, headers=headers).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    return None, None

# Ambil lokasi
if alamat_input:
    lat, lon = get_coordinates_from_address(alamat_input)
elif lat_param and lon_param:
    lat = float(lat_param)
    lon = float(lon_param)

# Tampilkan POS jika lokasi tersedia
if lat and lon:
    user_loc = (lat, lon)
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    # Tampilkan 3 POS dalam grid horizontal
    cols = st.columns(3)
    for idx, (i, row) in enumerate(top3.iterrows()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background-color:white; color:black; border-radius:10px; padding:15px; 
                         border:1px solid #ddd; margin-bottom:20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
                <div style="font-weight:bold; color:#005BAC; font-size: 16px;">📍 {i+1}. {row['POS Name']}</div>
                <div style="margin-bottom:6px; font-size:14px;">{row['alamat']}</div>
                <div style="font-size:13px;">📱 <a href="https://wa.me/{row['whatsapp']}" target="_blank">{row['whatsapp']}</a></div>
                <div style="font-size:13px;">🕐 {row['jam_buka']}</div>
                <div style="margin-top:10px;">
                    <a href="https://wa.me/{row['whatsapp']}" target="_blank"
                       style="background-color:#005BAC; color:white; padding:6px 12px; border-radius:5px;
                              text-decoration:none; margin-right:8px; font-size:13px;">Hubungi Cabang</a>
                    <a href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" 
                       target="_blank"
                       style="background-color:#005BAC; color:white; padding:6px 12px; border-radius:5px;
                              text-decoration:none; font-size:13px;">Petunjuk Arah</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Tampilkan peta
    st.subheader("🗺️ Lokasi di Peta")
    m = folium.Map(location=[lat, lon], zoom_start=13)
    folium.Marker(location=[lat, lon], popup="📍 Lokasi Anda", icon=folium.Icon(color="blue")).add_to(m)

    for _, row in top3.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=row["POS Name"],
            icon=folium.Icon(color="red")
        ).add_to(m)

    st_folium(m, width=700, height=500)

else:
    st.info("Silakan masukkan alamat atau gunakan URL dengan ?lat=...&lon=...")
