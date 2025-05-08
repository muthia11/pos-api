import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="POS Terdekat BFI", layout="centered")

# CSS for white background and font styling
st.markdown("""
    <style>
        .stApp { background-color: white !important; }
        html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# Logo BFI at the top
st.markdown("""
    <div style='text-align:center; margin-bottom: 10px;'>
        <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#005BAC;'>📍 Cek POS Terdekat</h2>", unsafe_allow_html=True)

alamat_input = st.text_input("Masukkan alamat Anda", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta")

# Fallback ke query param jika ada
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

# Nominatim
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

# Jika lokasi valid
if lat and lon:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    if len(top3) == 3:
        col1, col2, col3 = st.columns(3)
        for col, (_, row) in zip([col1, col2, col3], top3.iterrows()):
            with col:
                st.markdown(f"""
                    <div style="background-color:white; color:black; border-radius:10px; padding:15px; 
                                 border:1px solid #ddd; margin-bottom:20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
                        <div style="font-weight:bold; color:#005BAC; font-size: 16px;">📍 {row['POS Name']}</div>
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
    else:
        for _, row in top3.iterrows():
            st.markdown(f"""
                <div style="background-color:white; color:black; border-radius:10px; padding:15px; 
                             border:1px solid #ddd; margin-bottom:20px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
                    <div style="font-weight:bold; color:#005BAC; font-size: 16px;">📍 {row['POS Name']}</div>
                    <div style="margin-bottom:6px; font-size:14px;">{row['alamat']}</div>
                    <div style="font-size:13px;">📱 <a href="https://wa.me/{row['whatsapp']}" target="_blank">{row['whatsapp']}</a></div>
                    <div style="font-size:13px;">🕐 {row['jam_buka']}</div>
                    <div style="margin-top:10px;">
                        <a href="https://wa.me/{row[']()
