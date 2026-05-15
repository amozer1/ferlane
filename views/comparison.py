import streamlit as st
import plotly.graph_objects as go
from core.engine import build_dashboard

def render_comparison():

    data = build_dashboard()

    cl31 = data["cl31"]
    cl32 = data["cl32"]

    st.title("Baseline Comparison (CL31 vs CL32)")

    fig = go.Figure()

    if "Finish" in cl31.columns and "Finish" in cl32.columns:
        fig.add_trace(go.Scatter(y=cl31["Finish"], name="CL31"))
        fig.add_trace(go.Scatter(y=cl32["Finish"], name="CL32"))

    st.plotly_chart(fig, use_container_width=True)