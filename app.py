import streamlit as st
import pandas as pd
from utils.loader import load_programme_data, prepare_comparison_df
from components.deliverables import render_deliverables_table

st.set_page_config(page_title="CL31 vs CL32 Comparison", layout="wide")

st.title("📊 CL31 vs CL32 Programme Comparison Dashboard")

# File uploads
cl31_file = st.file_uploader("Upload CL31 Programme File", type=["xlsx", "csv"])
cl32_file = st.file_uploader("Upload CL32 Programme File", type=["xlsx", "csv"])

if cl31_file and cl32_file:
    # Load data
    df31 = load_programme_data(cl31_file)
    df32 = load_programme_data(cl32_file)

    # Build comparison dataset
    comparison_df = prepare_comparison_df(df31, df32)

    # Render table
    render_deliverables_table(comparison_df)

else:
    st.info("Please upload both CL31 and CL32 programme files to continue.")
