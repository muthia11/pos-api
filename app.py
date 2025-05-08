import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Konfigurasi dasar
st.set_page_config(page_title="POS Terdekat BFI", layout="centered")

# Paksa background putih untuk seluruh halaman
st.markdown("""
    <style>
        .stApp {
            background-color: white !important;
        }
    </style>
""", unsafe_allow_html=True)


# CSS styling agar tampilan bersih dan tetap terlihat di semua mode
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        .pos-card {
            background-color: white;
            color: black !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
        }
        .pos-title {
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 6px;
            color: #005BAC;
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
st.markdown("<h2 style='text-align:center; color:#005BAC;'>📍 Cek POS Terdekat</h2>", unsafe_allow_html=True)

# Input alamat
alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

# Fallback dari query param
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

# Fungsi geocoding alamat (Nominatim)
def get_coordinates_from_address(alamat):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": alamat, "format": "json", "limit": 1}
    headers = {"User-Agent": "streamlit-pos-app"}
    response = requests.get(url, params=params, headers=headers).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    return None, None

# Ambil lokasi pengguna
if alamat_input:
    lat, lon = get_coordinates_from_address(alamat_input)
elif lat_param and lon_param:
    lat = float(lat_param)
    lon = float(lon_param)

# Jika lat/lon valid, proses pencarian POS
if lat and lon:
    user_loc = (lat, lon)
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    for i, row in top3.iterrows():
        st.markdown(f"""
        <div class="pos-card">
            <div class="pos-title">📍 {i+1}. {row['POS Name']}</div>
            <div>{row['alamat']}</div>
            <div>📱 <a href="https://wa.me/{row['whatsapp']}" target="_blank">{row['whatsapp']}</a></div>
            <div>🕐 {row['jam_buka']}</div>
            <div class="btn-container">
                <a class="btn" href="https://wa.me/{row['whatsapp']}" target="_blank">Hubungi Cabang</a>
                <a class="btn" href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" target="_blank">Petunjuk Arah</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Peta interaktif
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
    st.info("Silakan masukkan alamat atau gunakan parameter ?lat=...&lon=... di URL.")
