import streamlit as st

from loader import load_cl31, load_cl32
from deliverables import build_deliverables
from layout.home_layout import render_home

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# GLOBAL STYLING
# =========================
st.markdown("""
<style>

.stApp {
    background-color: #140021;
}

/* REMOVE DEFAULT PADDING */
.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* CARD STYLE */
.dashboard-card {
    background-color: #240046;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
}

/* CARD TITLES */
.card-title {
    color: white;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 18px;
}

/* METRICS */
div[data-testid="stMetric"] {
    background-color: #3c096c;
    border-radius: 14px;
    padding: 14px;
    text-align: center;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

/* TEXT */
h1, h2, h3, h4, h5, h6, p, div {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("📊 CL31 vs CL32 Deliverable Dashboard")

# =========================
# LOAD DATA
# =========================
df31 = load_cl31()
df32 = load_cl32()

result = build_deliverables(df31, df32)

# =========================
# RENDER HOME
# =========================
render_home(result)