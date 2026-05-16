import streamlit as st
import pandas as pd
from utils.loader import load_and_prepare_files, prepare_comparison_df

st.set_page_config(page_title="CL31 vs CL32 Comparison", layout="wide")

st.title("CL31 vs CL32 Deliverable Comparison Dashboard")

# -----------------------------
# AUTO LOAD FILES
# -----------------------------
CL31_PATH = "data/CL31.xlsx"
CL32_PATH = "data/CL32.xlsx"

try:
    df31, df32 = load_and_prepare_files(CL31_PATH, CL32_PATH)

    result_df = prepare_comparison_df(df31, df32)

    st.success("Files loaded automatically from /data folder")

    st.subheader("Deliverable Comparison Table")
    st.dataframe(result_df, use_container_width=True)

except FileNotFoundError as e:
    st.error("Missing CL31 or CL32 file in /data folder")
    st.exception(e)