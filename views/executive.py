import streamlit as st
import plotly.express as px

from core.engine import build_dashboard
from components.cards import kpi_row

def render_executive():

    data = build_dashboard()

    st.title("FERLANE NEC Programme Controls")

    kpi_row(data)

    st.divider()

    df = data["cl32"]

    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig = px.bar(status_counts, x="Status", y="Count", title="CL32 Float Classification")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("NEC Programme Commentary")
    st.info(data["commentary"])