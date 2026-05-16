import streamlit as st
from loader import load_cl31, load_cl32
from deliverables import build_deliverables
from cards.chart_card import render_pie   # 👈 FIXED IMPORT PATH

st.set_page_config(layout="wide")

st.title("📊 CL31 vs CL32 Deliverable Tracker")

# =========================
# LOAD
# =========================
df31 = load_cl31()
df32 = load_cl32()

result = build_deliverables(df31, df32)

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(result))
col2.metric("NEW", (result["Change Type"] == "NEW").sum())
col3.metric("DELAYED", (result["Change Type"] == "DELAYED").sum())
col4.metric("EARLY", (result["Change Type"] == "EARLY").sum())

# =========================
# PIE CARD
# =========================
render_pie(result)

# =========================
# TABLE
# =========================
st.subheader("Deliverable Comparison Table")

st.dataframe(result, use_container_width=True, hide_index=True)