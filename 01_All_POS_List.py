import streamlit as st
import pandas as pd

st.set_page_config(page_title="Daftar POS BFI", layout="wide")

st.markdown("<h2 style='color:#005BAC;'>Daftar Lengkap POS BFI Finance</h2>", unsafe_allow_html=True)

df = pd.read_excel("pos_data.xlsx", engine="openpyxl")

st.dataframe(df[["POS Name", "alamat", "whatsapp", "jam_buka"]], use_container_width=True)
