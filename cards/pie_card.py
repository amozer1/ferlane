import streamlit as st
import plotly.express as px
import pandas as pd


def render_pie(result):

    pie_df = pd.DataFrame()

    pie_df["Programme Status"] = result["Change Type"].map({
        "UNCHANGED": "On Track",
        "DELAYED": "Delayed",
        "EARLY": "Accelerated"
    })

    pie_df = pie_df.dropna()

    summary = (
        pie_df["Programme Status"]
        .value_counts()
        .reset_index()
    )

    summary.columns = ["Status", "Count"]

    color_map = {
        "On Track": "gold",
        "Delayed": "red",
        "Accelerated": "green"
    }

    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map=color_map,
        hole=0.45
    )

    fig.update_layout(
        title="Programme Update",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="black",
        height=280,
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )