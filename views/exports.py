import streamlit as st
from core.engine import build_dashboard

def render_exports():

    data = build_dashboard()
    df = data["cl32"]

    st.title("Export Centre")

    st.download_button(
        "Download CL32 Data",
        df.to_csv(index=False),
        file_name="CL32_export.csv"
    )