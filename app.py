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

/* PAGE LAYOUT */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 100%;
}

/* REDUCE GAPS */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.6rem;
}

/* CARD */
.dashboard-card {
    background-color: #240046;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
}

/* CARD TITLE */
.card-title {
    color: white;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

/* METRICS */
div[data-testid="stMetric"] {
    background-color: #3c096c;
    border-radius: 10px;
    padding: 8px;
    text-align: center;
}

/* STREAMLIT DATAFRAME HEADERS */

[data-testid="stDataFrame"] div[role="columnheader"] {
    background-color: #3a3a3a !important;
    color: white !important;
    font-weight: 600 !important;
}
    border-radius: 10px;
    overflow: hidden;
}

/* TABLE HEADERS ONLY */
[data-testid="stDataFrame"] thead tr th {
    background-color: #3a3a3a !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

/* TEXT */
h1, h2, h3, h4, h5, h6, p, div {
    color: white;
}

/* TITLE SIZE */
h1 {
    font-size: 28px !important;
    margin-bottom: 10px !important;
}

/* PIE SPACING */
.js-plotly-plot {
    margin-top: -10px;
}

/* REMOVE EXTRA SPACE */
.element-container {
    margin-bottom: 0.4rem !important;
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
# RENDER DASHBOARD
# =========================
render_home(result, df32)