# =========================
# app.py
# =========================

import streamlit as st
from utils.loader import load_schedule
from components.deliverables import build_deliverables_card

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="FERLANE NEC Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

cl31, cl32 = load_schedule(
    "data/CL31.xlsx",
    "data/CL32.xlsx"
)

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------

st.title("FERLANE NEC Dashboard")

# ---------------------------------------------------
# DELIVERABLES CARD
# ---------------------------------------------------

build_deliverables_card(cl31, cl32)