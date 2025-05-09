import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daftar POS BFI", layout="wide")

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
        th {
            background-color: #005BAC !important;
            color: white !important;
        }
        td {
            font-size: 14px !important;
        }
    </style>
""", unsafe_allow_html=True)

# ===== HEADER & LOGO =====
st.markdown("""
    <div style='text-align:center; margin-bottom: 16px;'>
        <img src='https://raw.githubusercontent.com/muthia11/pos-api/ae84f4667e53e93832cd41c2047753d4ca6984bd/bfi-logo.png' width='120'/>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <h2 style='text-align:center; color:#005BAC;'>Daftar Lengkap POS BFI Finance</h2>
    <p style='text-align:center; font-size:16px;'>Temukan seluruh cabang POS BFI di Indonesia</p>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
try:
    df = pd.read_excel("pos_data.xlsx", engine="openpyxl")
    df_view = df[["POS Name", "alamat", "whatsapp", "jam_buka"]].copy()
    df_view.columns = ["Nama POS", "Alamat", "WhatsApp", "Jam Buka"]
    st.dataframe(df_view, use_container_width=True)
except Exception as e:
    st.error(f"Gagal memuat data POS. Periksa file Excel. Error: {e}")
