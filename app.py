import streamlit as st

from loader import load_cl31, load_cl32
from deliverables import build_deliverables
from layout.home_layout import render_home   # 👈 NEW

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# DARK PURPLE THEME (GLOBAL)
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #12001f;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #1a0033;
    }

    div[data-testid="stMetric"] {
        background-color: #240046;
        padding: 15px;
        border-radius: 12px;
        color: white;
    }

    .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
render_home(result)