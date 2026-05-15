import streamlit as st
import plotly.express as px
from core.engine import build_dashboard

def render_analytics():

    data = build_dashboard()
    df = data["cl32"]

    st.title("Float Analytics")

    fig = px.histogram(df, x="Float", nbins=20)
    st.plotly_chart(fig, use_container_width=True)