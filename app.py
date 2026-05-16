import streamlit as st
from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables

st.set_page_config(
    page_title="CL31 vs CL32 Dashboard",
    layout="wide"
)

st.title("📊 CL31 vs CL32 Programme Dashboard")

# ---------------------------------
# AUTO LOAD FILES
# ---------------------------------
CL31_FILE = "data/CL31-February.xlsx"
CL32_FILE = "data/CL32-May.xlsx"

# load automatically
df = prepare_comparison_df(CL31_FILE, CL32_FILE)

# render table
render_deliverables(df)