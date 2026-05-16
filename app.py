import streamlit as st
import pandas as pd

from loader import load_schedule
from deliverables import build_deliverables

st.set_page_config(layout="wide")

st.title("📊 CL31 vs CL32 Deliverable Tracker")


# =========================
# LOAD FILES (FROM DATA FOLDER)
# =========================
CL31_PATH = "data/CL31-February.xlsx"
CL32_PATH = "data/CL32-May.xlsx"

df31 = load_schedule(CL31_PATH)
df32 = load_schedule(CL32_PATH)


# =========================
# BUILD DELIVERABLE TABLE
# =========================
result = build_deliverables(df31, df32)


# =========================
# FILTERS (SIDEBAR)
# =========================
st.sidebar.header("Filters")

status_options = result["Change Type"].unique()

selected_status = st.sidebar.multiselect(
    "Change Type",
    options=status_options,
    default=status_options
)

filtered = result[result["Change Type"].isin(selected_status)]


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
    filtered,
    use_container_width=True,
    hide_index=True
)