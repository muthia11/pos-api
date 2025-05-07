import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import requests
import folium
from streamlit_folium import st_folium

# ============== KONFIGURASI DASAR ==============
BFI_BLUE = "#005BAC"
LOGO_URL = "https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png"

st.set_page_config(page_title="POS Terdekat BFI", page_icon="📍", layout="centered")

# ============== CSS KHUSUS ==============
st.markdown(f"""
    <style>
        body {{
            background-color: white;
            font-family: 'Segoe UI', sans-serif;
        }}
        .logo {{
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }}
        .nav {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .nav a {{
            margin: 0 15px;
            color: {BFI_BLUE};
            font-weight: bold;
            text-decoration: none;
        }}
        .card {{
            background-color: #fff;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 20px;
            box-shadow: 2px 4px 10px rgba(0,0,0,0.05);
        }}
        .card h5 {{
            color: {BFI_BLUE};
        }}
        .btn {{
            background-color: {BFI_BLUE};
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            text-decoration: none;
        }}
    </style>
""", unsafe_allow_html=True)

# ============== LOGO & NAVBAR ==============
st.markdown(f"""
    <div class="logo">
        <img src="{LOGO_URL}" width="100"/>
    </div>
    <div class="nav">
        <a href="#tentang-pos">Tentang POS</a>
        <a href="#cek-pos-terdekat">Cek POS Terdekat</a>
        <a href="#hubungi-kami">Hubungi Kami</a>
    </div>
""", unsafe_allow_html=True)

# ============== TENTANG POS ==============
st.markdown("<h3 id='tentang-pos'>📘 Tentang POS</h3>", unsafe_allow_html=True)
st.write("""
POS (Point of Service) BFI Finance adalah titik layanan konsumen untuk mengajukan pembiayaan kendaraan menggunakan jaminan BPKB motor atau mobil. 
POS hadir lebih dekat ke masyarakat agar proses pengajuan lebih cepat, mudah, dan nyaman.
""")

# ============== INPUT ALAMAT USER ==============
st.markdown("<h3 id='cek-pos-terdekat'>📍 Cek POS Terdekat</h3>", unsafe_allow_html=True)
alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

if alamat_input:
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": alamat_input, "format": "json", "limit": 1}
    headers = {"User-Agent": "streamlit-pos-bfi"}
    response = requests.get(url, params=params, headers=headers).json()
    if response:
        lat = float(response[0]['lat'])
        lon = float(response[0]['lon'])
elif lat_param and lon_param:
    lat = float(lat_param)
    lon = float(lon_param)

# ============== LOGIKA CARI POS TERDEKAT ==============
if lat and lon:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    for i, row in top3.iterrows():
        st.markdown(f"""
        <div class="card">
            <h5>📌 {i+1}. {row['POS Name']}</h5>
            <p>{row['alamat']}</p>
            <a href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" target="_blank" class="btn">📍 Ke Lokasi</a>
        </div>
        """, unsafe_allow_html=True)

    # MAP
    st.markdown(f"<h4 style='color:{BFI_BLUE}'>🗺️ Lokasi di Peta</h4>", unsafe_allow_html=True)
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
    st.info("Silakan masukkan alamat atau akses link dengan parameter `?lat=...&lon=...`.")

# ============== HUBUNGI KAMI ==============
st.markdown("<h3 id='hubungi-kami'>📞 Hubungi Kami</h3>", unsafe_allow_html=True)
st.write("""
Jika Anda memiliki pertanyaan lebih lanjut terkait lokasi POS atau layanan kami, silakan hubungi:

📧 Email: cs@bfi.co.id  
📞 Telepon: 1500018  
🌐 Website: [https://www.bfi.co.id](https://www.bfi.co.id)
""")
