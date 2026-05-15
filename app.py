import streamlit as st

from utils.loader import load_programme_data
from components.cl32_card import render_cl32_card

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="FERLANE NEC Controls", layout="wide")

st.title("FERLANE NEC Programme Controls Dashboard")
st.caption("CL31 vs CL32 Deliverable Movement")

st.divider()

# -----------------------------
# LOAD DATA
# -----------------------------
cl31, cl32 = load_programme_data()

# -----------------------------
# CARD 1 ONLY
# -----------------------------
render_cl32_card(cl31, cl32)