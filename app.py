import streamlit as st

from loader import load_cl31, load_cl32
from deliverables import build_deliverables
from layout.home_layout import render_home
from cards.table_card import render_table  # reuse existing card


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(layout="wide")

# =========================
# STYLING (UNCHANGED)
# =========================
st.markdown("""<style>
.stApp { background-color: #140021; }
.block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; max-width: 100%; }
div[data-testid="stVerticalBlock"] > div { gap: 0.6rem; }
.dashboard-card {
    background-color: #240046;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.06);
    box-shadow: 0px 3px 10px rgba(0,0,0,0.25);
}
.card-title {
    color: white;
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}
h1, h2, h3, h4, h5, h6, p, div { color: white; }
h1 { font-size: 28px !important; margin-bottom: 10px !important; }
</style>""", unsafe_allow_html=True)


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
# NAVIGATION (SIMPLE)
# =========================
page = st.sidebar.selectbox(
    "Navigation",
    ["Overview (CL32)", "Deliverable Register"]
)


# =========================
# PAGE 1 — OVERVIEW
# =========================
if page == "Overview (CL32)":
    render_home(result, df32)


# =========================
# PAGE 2 — REGISTER (NO EXTRA FILE)
# =========================
elif page == "Deliverable Register":

    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">📋 CL31 vs CL32 Deliverable Register</div>
    """, unsafe_allow_html=True)

    render_table(result)

    st.markdown("</div>", unsafe_allow_html=True)