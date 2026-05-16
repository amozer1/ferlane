import streamlit as st
from utils.loader import load_file, prepare_comparison_df
from components.deliverables import render_table, render_summary

st.set_page_config(page_title="CL31 vs CL32 Tracker", layout="wide")

st.title("📊 Deliverable Comparison Dashboard (CL31 vs CL32)")


# ---------------------------
# AUTO LOAD FILES (NO UPLOAD)
# ---------------------------
CL31_PATH = "data/CL31.xlsx"
CL32_PATH = "data/CL32.xlsx"


df31 = load_file(CL31_PATH)
df32 = load_file(CL32_PATH)


# ---------------------------
# PROCESS
# ---------------------------
comparison_df = prepare_comparison_df(df31, df32)


# ---------------------------
# DISPLAY
# ---------------------------
render_summary(comparison_df)
render_table(comparison_df)