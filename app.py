import streamlit as st
from loader import load_schedule
from deliverables import build_deliverables

st.set_page_config(layout="wide")

st.title("📊 CL31 vs CL32 Deliverable Tracker")

# =========================
# LOAD DATA
# =========================
df31 = load_schedule("data/CL31-February.xlsx")
df32 = load_schedule("data/CL32-May.xlsx")

# =========================
# BUILD TABLE
# =========================
result = build_deliverables(df31, df32)

# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(result))
col2.metric("NEW", (result["Change Type"] == "NEW").sum())
col3.metric("DELAYED", (result["Change Type"] == "DELAYED").sum())
col4.metric("UNCHANGED", (result["Change Type"] == "UNCHANGED").sum())

# =========================
# TABLE
# =========================
st.subheader("Deliverable Comparison Table")

st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)