import streamlit as st
from core.engine import build_dashboard

def render_critical():

    data = build_dashboard()
    df = data["cl32"]

    st.title("Critical Path Register")

    critical = df[df["Status"] == "Critical"]

    st.dataframe(critical, use_container_width=True)