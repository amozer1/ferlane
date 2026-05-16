import streamlit as st
import pandas as pd
from loader import load_cl31, load_cl32
from deliverables import build_deliverables


st.set_page_config(layout="wide")
st.title("📊 CL31 vs CL32 Deliverable Tracker")


# =========================
# LOAD DATA
# =========================
df31 = load_cl31("data/CL31-February.xlsx")
df32 = load_cl32("data/CL32-May.xlsx")

result = build_deliverables(df31, df32)


# =========================
# COLOUR FUNCTIONS (NEW API)
# =========================
def color_change(val):
    if val == "NEW":
        return "background-color:#c6f6c6"
    if val == "DELAYED":
        return "background-color:#ffd1d1"
    if val == "EARLY":
        return "background-color:#cce5ff"
    if val == "REMOVED":
        return "background-color:#e0e0e0"
    return ""


def color_delta(val):
    if pd.isna(val):
        return ""
    if isinstance(val, (int, float)):
        if val > 0:
            return "color:red"
        if val < 0:
            return "color:green"
    return ""


# =========================
# APPLY STYLING (FIXED)
# =========================
styled = result.style

# Pandas 2.x replacement for applymap
styled = styled.map(color_change, subset=["Change Type"])
styled = styled.map(color_delta, subset=["Delta (Days)"])


# =========================
# KPI CARDS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(result))
col2.metric("NEW", (result["Change Type"] == "NEW").sum())
col3.metric("DELAYED", (result["Change Type"] == "DELAYED").sum())
col4.metric("EARLY", (result["Change Type"] == "EARLY").sum())


# =========================
# TABLE
# =========================
st.subheader("Deliverable Comparison (CL31 vs CL32)")

st.dataframe(
    styled,
    use_container_width=True,
    hide_index=True
)