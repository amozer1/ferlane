import streamlit as st
from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables

# FILES (your renamed ones)
CL31_FILE = "CL31-February.xlsx"
CL32_FILE = "CL32-May.xlsx"


st.set_page_config(layout="wide", page_title="Programme Comparison Dashboard")

st.title("📊 CL31 vs CL32 Programme Comparison")


# AUTO LOAD (NO UPLOAD REQUIRED)
df = prepare_comparison_df(CL31_FILE, CL32_FILE)

render_deliverables(df)