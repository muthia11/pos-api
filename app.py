import streamlit as st
import pandas as pd
import requests
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="POS BFI Terdekat", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    html, body {
        background-color: white !important;
        overflow-x: hidden;
    }
    input::placeholder {
        color: #666 !important;
        opacity: 1 !important;
    }
    </style>
""", unsafe_allow_html=True)



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

st.markdown("""
<div style='text-align: center; color: #005BAC; line-height: 1.3;'>
  <h2 style='margin-bottom: 0; font-weight: bold;'>POS BFI Finance</h2>
  <p style='font-size: 25px; margin-top: 4px;'>Temui Kami Lebih Dekat</p>
</div>
""", unsafe_allow_html=True)

# Input alamat
st.markdown("Masukkan alamat Anda")
alamat_input = st.text_input("", placeholder="Contoh: Jl. Sudirman No. 10, Jakarta", label_visibility="collapsed")

# CSS tambahan untuk placeholder
st.markdown("""
    <style>
    input::placeholder {
        color: #666 !important;  /* atau pakai #000 untuk hitam */
        opacity: 1 !important;   /* pastikan tidak transparan */
    }
    </style>
""", unsafe_allow_html=True)


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


# Tombol untuk menampilkan semua daftar POS
show_all = st.button("📄 Lihat Semua Daftar Cabang POS BFI")

st.markdown("""
<a href="https://pos-api-fyxnm84xudbbvk5nmyhbxb.streamlit.app/?page=Daftar%20POS%20BFI" target="_self">
    <div style="display:inline-block; background-color:#005BAC; color:white; padding:10px 16px; border-radius:6px; font-size:14px; text-decoration:none;">
        📄 Lihat Semua Daftar Cabang POS BFI
    </div>
</a>
""", unsafe_allow_html=True)



# # Judul
# st.markdown("<h4 style='color:#005BAC;'>Daftar Lengkap POS BFI Finance</h4>", unsafe_allow_html=True)

# # Style dan tampilan tabel
# st.markdown("""
#     <style>
#         /* Background putih dan teks gelap */
#         [data-testid="stDataFrame"] {
#             background-color: white !important;
#             color: black !important;
#         }

#         /* Header tabel warna biru BFI */
#         [data-testid="stDataFrame"] thead tr th {
#             background-color: white !important;
#             color: #005BAC !important;
#             font-weight: bold;
#             font-size: 13px;
#         }

#         /* Teks isi tabel */
#         [data-testid="stDataFrame"] tbody td {
#             color: black !important;
#             font-size: 12px;
#         }
#     </style>
# """, unsafe_allow_html=True)


# Render table manually
def render_custom_table(df):
    html = '<table class="custom-table">'
    # Header
    html += '<tr>' + ''.join(f'<th>{col}</th>' for col in df.columns) + '</tr>'
    # Rows
    for _, row in df.iterrows():
        html += '<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
    html += '</table>'
    st.dataframe(df_view, use_container_width=True)

# Load data and show
try:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    df_view = df[["POS Name", "alamat", "whatsapp", "jam_buka"]].copy()
    df_view.columns = ["Nama POS", "Alamat", "WhatsApp", "Jam Buka"]
    render_custom_table(df_view)
except Exception as e:
    st.error(f"Gagal memuat data POS: {e}")





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


# ====== FOOTER ======
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

