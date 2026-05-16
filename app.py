import streamlit as st
import pandas as pd

from utils.loader import load_and_prepare_files, prepare_comparison_df

st.set_page_config(page_title="CL31 vs CL32 Comparison", layout="wide")

st.title("CL31 vs CL32 Deliverable Comparison Dashboard")

st.markdown("Upload CL31 and CL32 programme files (Excel).")

file31 = st.file_uploader("Upload CL31 Programme", type=["xlsx"])
file32 = st.file_uploader("Upload CL32 Programme", type=["xlsx"])

if file31 and file32:

    # Load + preprocess
    df31, df32 = load_and_prepare_files(file31, file32)

    # Comparison
    result_df = prepare_comparison_df(df31, df32)

    st.subheader("Deliverable Comparison Table")
    st.dataframe(result_df, use_container_width=True)

else:
    st.info("Please upload both CL31 and CL32 files to continue.")