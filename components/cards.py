import streamlit as st

def kpi_row(data):

    k = data["kpis"]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Activities", k["total"])
    col2.metric("Critical", k["critical"])
    col3.metric("Near Critical", k["near_critical"])
    col4.metric("Non Critical", k["non_critical"])
    col5.metric("Avg Float", f"{k['avg_float']:.1f} days")