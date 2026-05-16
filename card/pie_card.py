import streamlit as st
import plotly.express as px


def render_pie(result):
    st.subheader("Programme Health Summary")

    summary = result["Change Type"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]

    color_map = {
        "DELAYED": "red",
        "EARLY": "green",
        "UNCHANGED": "gold",
        "NEW": "orange",
        "REMOVED": "lightgrey"
    }

    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map=color_map,
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)