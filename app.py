import streamlit as st
from utils.loader import prepare_comparison_df
from components.deliverables import render_table, render_structured_view

st.set_page_config(layout="wide")

st.title("📊 CL Programme Comparison Dashboard")

# NEW FILE NAMES
CL31_FILE = "data/CL31-February.xlsx"
CL32_FILE = "data/CL-May.xlsx"

# AUTO LOAD
df = prepare_comparison_df(CL31_FILE, CL32_FILE)

tab1, tab2 = st.tabs(["📊 Comparison Table", "🧭 Structured View"])

with tab1:
    render_table(df)

with tab2:
    render_structured_view(df)