import streamlit as st
import pandas as pd
from utils.loader import load_programme
from components.deliverables import extract_deliverables, build_deliverables_card

st.set_page_config(layout="wide")

st.title("Deliverable Tracker Dashboard")

# -------------------------
# AUTO FILE PATHS
# -------------------------
CL31_PATH = "data/CL31.xlsx"
CL32_PATH = "data/CL32.xlsx"


@st.cache_data
def load_data():
    cl31_df = load_programme(CL31_PATH)
    cl32_df = load_programme(CL32_PATH)
    return cl31_df, cl32_df


try:
    cl31_df, cl32_df = load_data()

    df = pd.concat([cl31_df, cl32_df], ignore_index=True)

    deliverables_df = extract_deliverables(df)
    final_df = build_deliverables_card(deliverables_df)

    st.subheader("Schedule Summary")

    st.dataframe(final_df, use_container_width=True, hide_index=True)

except FileNotFoundError as e:
    st.error(f"Missing file: {e}")
    st.info("Ensure CL31.xlsx and CL32.xlsx are inside the /data folder.")