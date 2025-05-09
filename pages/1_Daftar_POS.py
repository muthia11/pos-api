import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(page_title="Daftar POS", layout="wide")

# ===== STYLE GLOBAL =====
st.markdown("""
    <style>
        html, body {
            background-color: white !important;
            font-family: 'Segoe UI', sans-serif;
        }
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER & LOGO =====
st.markdown("""
    <div style='text-align:center; margin-bottom: 16px;'>
        <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
    </div>
""", unsafe_allow_html=True)

# ===== TOMBOL KEMBALI =====
st.markdown("""
<a href="https://pos-api-fyxnm84xudbbvk5nmyhbxb.streamlit.app" target="_self">
    <div style="
        display: inline-block;
        background-color: #888;
        color: white;
        padding: 8px 14px;
        border-radius: 6px;
        font-size: 13px;
        text-decoration: none;
        margin-bottom: 10px;
        cursor: pointer;">
        ⬅️ Kembali ke Halaman Utama
    </div>
</a>
""", unsafe_allow_html=True)

# ===== JUDUL =====
st.markdown("<h4 style='color:#005BAC;'>Daftar Lengkap POS BFI Finance</h4>", unsafe_allow_html=True)
st.markdown("<p style='font-size:14px;'>Klik tombol 'Arahkan' untuk membuka rute ke lokasi POS.</p>", unsafe_allow_html=True)

# ===== LOAD DATA & TABEL =====
try:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

    # Ambil kolom utama + koordinat
    df_view = df[["POS Name", "alamat", "whatsapp", "jam_buka", "lat", "lon"]].copy()
    df_view.columns = ["Nama POS", "Alamat", "WhatsApp", "Jam Buka", "lat", "lon"]

    # Tambahkan kolom tombol arahkan
    df_view["Arahkan"] = df_view.apply(
        lambda row: f'<a href="https://www.google.com/maps/dir/?api=1&destination={row["lat"]},{row["lon"]}" target="_blank"><div style="background-color:#005BAC; color:white; padding:4px 10px; border-radius:5px; font-size:12px; text-align:center;">Arahkan</div></a>',
        axis=1
    )

    # Tampilkan hanya kolom yang dibutuhkan
    df_display = df_view[["Nama POS", "Alamat", "WhatsApp", "Jam Buka", "Arahkan"]]

    # HTML Table with CSS Styling
    html_table = f"""
    <style>
        .custom-table-wrapper {{
            overflow-x: auto;
            max-height: 500px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Segoe UI', sans-serif;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
        }}

        th {{
            background-color: #005BAC;
            color: white;
            padding: 8px;
            font-size: 13px;
            text-align: left;
        }}

        td {{
            border-top: 1px solid #eee;
            padding: 8px;
            font-size: 12px;
            color: #333;
            vertical-align: top;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        a .btn {{
            background-color: #005BAC;
            color: white;
            padding: 4px 10px;
            border-radius: 5px;
            font-size: 12px;
            text-align: center;
            display: inline-block;
            text-decoration: none;
        }}

        a .btn:hover {{
            background-color: #003f7d;
        }}
    </style>

    <div class="custom-table-wrapper">
        {df_display.to_html(escape=False, index=False)}
    </div>
    """

    components.html(html_table, height=600, scrolling=True)

except Exception as e:
    st.error(f"Gagal memuat data POS. Periksa file Excel. Error: {e}")
