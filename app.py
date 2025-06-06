import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="POS BFI Terdekat", layout="centered")

# ======== STYLE ========
st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    html, body {
        background-color: white !important;
        overflow-x: hidden;
    }
    input::placeholder {
        color: #666 !important;
        opacity: 1 !important;
    }
    .stApp {
        background-color: white !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
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


# ======== LOGO & JUDUL ========
# st.markdown("""
#     <div style='text-align:center; margin-bottom: 10px;'>
#         <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
#     </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div style='text-align: center; color: #005BAC; line-height: 1.4; margin-top: -12px;'>
#     <h2 style='margin-bottom: 6px; font-weight: 700; font-size: 30px;'>POS BFI Finance</h2>
#     <p style='font-size: 18px; margin: 0 auto; max-width: 280px;'>Temui Kami Lebih Dekat</p>
# </div>
# """, unsafe_allow_html=True)
# with st.container():
#     st.markdown("""
#     <div style="
#         display: flex;
#         flex-direction: column;
#         align-items: center;
#         padding: 40px 20px;
#         background-color: #F5F9FF;
#         border-radius: 12px;
#         margin-bottom: 24px;
#     ">
#         <div style="text-align: center;">
#             <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png'
#                  width='120' style="margin-bottom: 12px; display: block; margin-left: auto; margin-right: auto;" />
#             <h2 style="color: #005BAC; margin-bottom: 10px; font-size: 30px; font-weight: bold;">POS BFI Finance</h2>
#             <p style="font-size: 18px; margin-bottom: 4px;">Temui Kami Lebih Dekat</p>
#             <p style="font-size: 14px; color: #444;">Akses layanan pembiayaan BPKB dengan cepat dan mudah</p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# ======== HERO SECTION DENGAN BACKGROUND GAMBAR ========
st.markdown("""
<style>
.header-banner {
    position: relative;
    width: 100%;
    max-width: 960px;
    margin: 0 auto 20px auto;
    height: 170px;
    overflow: hidden;
    border-radius: 12px;
    background-image: url('https://raw.githubusercontent.com/muthia11/pos-api/main/pos-banner.png');
    background-size: cover;
    background-position: center;
}

.header-banner::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 45, 100, 0.8);  /* BFI dark blue with stronger transparency */
}

.header-text {
    position: relative;
    z-index: 2;
    color: white;
    text-align: center;
    padding: 25px 20px;
}

.header-text h2 {
    margin-bottom: 8px;
    font-size: 26px;
    font-weight: 700;
}

.header-text p {
    font-size: 15px;
    margin: 0;
}
</style>

<div class="header-banner">
  <div class="header-text">
    <h2>POS BFI Finance</h2>
    <p>Temui Kami Lebih Dekat</p>
    <p style="font-size: 13px; margin-top: 4px;">Akses layanan pembiayaan BPKB dengan cepat dan mudah</p>
  </div>
</div>
""", unsafe_allow_html=True)





# ======== FORM INPUT ALAMAT ========
with st.form("form_alamat"):
    st.markdown("**Masukkan alamat Anda**")
    alamat_input = st.text_input(
        "", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta", label_visibility="collapsed"
    )
    submit_clicked = st.form_submit_button("🔍 Cari POS Terdekat")


# ======== GEOCODING GOOGLE API ========
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

def get_coordinates_from_address(alamat):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": alamat, "key": GOOGLE_API_KEY}
    try:
        response = requests.get(url, params=params).json()
        if response["status"] == "OK":
            location = response["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    except Exception as e:
        st.error("Gagal mengambil koordinat dari Google API.")
    return None, None

# ======== CEK ALAMAT & HITUNG JARAK ========
query_params = st.query_params
lat_param, lon_param = query_params.get("lat"), query_params.get("lon")
lat = lon = None
source = None  # Tambahan variabel untuk menandai asal koordinat

if submit_clicked and alamat_input:
    lat, lon = get_coordinates_from_address(alamat_input)
    source = "input"
    st.text_input("Alamat Anda", value=alamat_input, disabled=True)

elif lat_param and lon_param:
    lat = float(lat_param)
    lon = float(lon_param)
    source = "auto"

if lat and lon:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    user_loc = (lat, lon)
    df["distance_km"] = df.apply(lambda row: geodesic(user_loc, (row["lat"], row["lon"])).km, axis=1)
    top3 = df.sort_values("distance_km").head(3)

    # 💬 Notifikasi berdasarkan asal koordinat
    if source == "input":
        st.success("Berikut adalah POS terdekat dari alamat yang Anda masukkan.")
    elif source == "auto":
        st.success("Berikut Top 3 POS terdekat dengan lokasi Anda saat ini.")

    # 💳 Tampilkan 3 POS terdekat
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

# ======== LINK KE HALAMAN DAFTAR POS ========
st.markdown("""
<a href="https://pos-api-fyxnm84xudbbvk5nmyhbxb.streamlit.app/Daftar_POS" target="_self">
    <div style="
        display: inline-block;
        background-color: #005BAC;
        color: white;
        padding: 10px 16px;
        border-radius: 6px;
        font-size: 14px;
        text-decoration: none;
        font-weight: bold;
        cursor: pointer;">
        📄 Lihat Semua Daftar Cabang POS BFI
    </div>
</a>
""", unsafe_allow_html=True)

# ======== FOOTER ========
st.markdown("""
<hr style='margin-top: 30px;'/>

<div style="display: flex; justify-content: space-between; flex-wrap: wrap; background-color:#005BAC; color:white; padding: 16px 20px; border-radius: 0px;">

  <div style="flex: 1; min-width: 240px; margin-right: 20px;">
    <h4 style="margin-bottom: 8px; font-size: 15px;">PT BFI Finance Indonesia Tbk</h4>
    <p style="margin:0; font-size:13px;">BFI Tower</p>
    <p style="margin:0; font-size:13px;">Sunburst CBD Lot. 1.2</p>
    <p style="margin:0; font-size:13px;">Jl. Kapt. Soebijanto Djojohadikusumo</p>
    <p style="margin:0; font-size:13px;">BSD City - Tangerang Selatan 15322</p>
    <p style="margin:10px 0 0; font-size:13px;">📞 +62 21 2965 0300, 2965 0500</p>
    <p style="margin:0; font-size:13px;">📠 +62 21 2965 0757, 2965 0758</p>
  </div>

  <div style="flex: 1; min-width: 240px;">
    <h4 style="margin-bottom: 8px; font-size: 15px;">Customer Care</h4>
    <p style="font-size: 18px; font-weight: bold; margin: 0;">1500018</p>
  </div>

</div>

<p style="text-align:center; margin-top: 12px; font-size: 12px; color: grey;">
  BFI Finance berizin dan diawasi oleh Otoritas Jasa Keuangan
</p>
""", unsafe_allow_html=True)
