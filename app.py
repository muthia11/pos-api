import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="POS BFI Terdekat", layout="centered")

# ======== FIX SCROLL DAN BACKGROUND PUTIH ==========
st.markdown("""
    <style>
        html, body {
            background-color: white !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow-x: hidden !important;
        }
        .stApp {
            background-color: white !important;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 0rem !important;
        }
        footer, header {visibility: hidden;}
        .element-container:has(.folium-map) {
            background-color: white !important;
            padding: 0px !important;
            margin: 0px !important;
        }
        iframe {
            margin-bottom: 0px !important;
        }
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        div[data-baseweb="input"] input {
            background-color: white !important;
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# Logo dan Judul
st.markdown("""
    <div style='text-align:center; margin-bottom: 10px;'>
        <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center; color:#005BAC;'>📍 POS BFI Finance – Temui Kami Lebih Dekat</h2>", unsafe_allow_html=True)

# Input alamat
st.markdown("Masukkan alamat Anda")
alamat_input = st.text_input("", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta", label_visibility="collapsed")

# Query param fallback
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None

# Geocoding
def get_coordinates_from_address(alamat):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": alamat, "format": "json", "limit": 1}
    headers = {"User-Agent": "streamlit-pos-app"}
    response = requests.get(url, params=params, headers=headers).json()
    if response:
        return float(response[0]['lat']), float(response[0]['lon'])
    return None, None

# Hitung lokasi terdekat
if alamat_input:
    lat, lon = get_coordinates_from_address(alamat_input)
elif lat_param and lon_param:
    lat = float(lat_param)
    lon = float(lon_param)

if lat and lon:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

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
                    <div style="margin-top:10px; display:flex; flex-direction:column;">
                        <a href="https://wa.me/{row['whatsapp']}" target="_blank"
                           style="background-color:#005BAC; color:white; padding:6px 12px; border-radius:5px;
                                  text-decoration:none; font-size:13px; margin-bottom:8px;">Hubungi Cabang</a>
                        <a href="https://www.google.com/maps/dir/?api=1&destination={row['lat']},{row['lon']}" 
                           target="_blank"
                           style="background-color:#005BAC; color:white; padding:6px 12px; border-radius:5px;
                                  text-decoration:none; font-size:13px;">Arahkan</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Peta
#     st.subheader("🗺️ Lokasi di Peta")
#     m = folium.Map(location=[lat, lon], zoom_start=13)
#     folium.Marker(location=[lat, lon], popup="📍 Lokasi Anda", icon=folium.Icon(color="blue")).add_to(m)
#     for _, row in top3.iterrows():
#         folium.Marker(
#             location=[row["lat"], row["lon"]],
#             popup=row["POS Name"],
#             icon=folium.Icon(color="red")
#         ).add_to(m)
#     st_folium(m, width=700, height=500)
# else:
#     st.info("Silakan masukkan alamat atau gunakan URL dengan ?lat=...&lon=...")


st.markdown(
    """
    <div style="position: relative; left: 0; right: 0; width: 100vw; margin: 0 -3rem; background-color:#005BAC; color:white; padding: 30px 40px 20px; box-sizing: border-box;">
      <div style="display: flex; justify-content: space-between; flex-wrap: wrap; max-width: 1200px; margin: auto;">
        <div style="flex: 1; min-width: 250px; margin-right: 40px;">
          <h4 style="margin-bottom: 10px;">PT BFI Finance Indonesia Tbk</h4>
          <p style="margin:0;">BFI Tower</p>
          <p style="margin:0;">Sunburst CBD Lot. 1.2</p>
          <p style="margin:0;">Jl. Kapt. Soebijanto Djojohadikusumo</p>
          <p style="margin:0;">BSD City - Tangerang Selatan 15322</p>
          <p style="margin:15px 0 0;">📞 +62 21 2965 0300, 2965 0500</p>
          <p style="margin:0;">📠 +62 21 2965 0757, 2965 0758</p>
        </div>
        <div style="flex: 1; min-width: 250px;">
          <h4 style="margin-bottom: 10px;">Customer Care</h4>
          <p style="font-size: 22px; font-weight: bold;">1500018</p>
        </div>
      </div>
      <p style="text-align:center; margin-top: 20px; font-size: 14px; color: #e0e0e0;">
        BFI Finance berizin dan diawasi oleh Otoritas Jasa Keuangan
      </p>
    </div>
    """,
    unsafe_allow_html=True
)




