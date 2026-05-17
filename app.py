import streamlit as st

from loader import load_cl31, load_cl32
from deliverables import build_deliverables
from layout.home_layout import render_home, render_register


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

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
# PAGE ROUTING ONLY
# =========================
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview (CL32)", "Deliverable Register"]
)

if page == "Overview (CL32)":
    render_home(result, df32)

elif page == "Deliverable Register":
    render_register(result)