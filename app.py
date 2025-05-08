import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Theme config
st.set_page_config(page_title="POS Terdekat BFI", layout="centered")

# CSS styling that works for both light/dark mode
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .pos-card {
            background-color: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(200,200,200,0.2);
        }
        .pos-title {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 6px;
        }
        .btn-container {
            margin-top: 12px;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            margin-right: 10px;
            border-radius: 6px;
            color: white;
            background-color: #005BAC;
            text-decoration: none;
        }
    </style>
""", unsafe_allow_html=True)

# Judul utama
st.markdown("<h2 style='text-align:center; color:#005BAC;'>📍 Cari POS Terdekat BFI</h2>", unsafe_allow_html=True)

# Input alamat
alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

# Query param fallback
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

# Nominatim API
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

# Jika lokasi ditemukan
if lat and lon:
    user_loc = (lat, lon)
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    for i, row in top3.iterrows():
        st.markdown(f"""
            <div class="pos-card">
                <div class="pos-title">📌 {row['POS Name']}</div>
                <div>{row['alamat']}</div>
                <div>📱 <a href="https://wa.me/{row['whatsapp']}" target="_blank">{row['whatsapp']}</a></div>
                <div>🕐 {row['jam_buka']}</div>
                <div class="btn-container">
                    <a class="btn" href="https://wa.me/{row['whatsapp']}" target="_blank">Hubungi Cabang</a>
                    <a class="btn" href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" target="_blank">Petunjuk Arah</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Map interaktif
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
    st.info("Silakan masukkan alamat atau gunakan URL dengan parameter ?lat=...&lon=...")

