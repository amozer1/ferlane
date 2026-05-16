import streamlit as st
from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables

st.set_page_config(layout="wide")

st.title("Deliverables Dashboard (CL31 vs CL32)")

st.caption("Auto-loading CL31-May and CL32-May from repository")

try:
    df = prepare_comparison_df()

    if df.empty:
        st.error("No data found in CL31/CL32 files")
    else:
        render_deliverables(df)

except FileNotFoundError as e:
    st.error("Missing required data files in /data folder")
    st.exception(e)

except Exception as e:
    st.error("Error processing programme data")
    st.exception(e)