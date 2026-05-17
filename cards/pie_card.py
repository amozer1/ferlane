import streamlit as st
import plotly.express as px
import pandas as pd


def render_pie(result):

    # =========================
    # CREATE STATUS
    # =========================
    pie_df = pd.DataFrame()

    pie_df["Programme Status"] = result["Change Type"].map({
        "UNCHANGED": "On Track",
        "DELAYED": "Delayed",
        "EARLY": "Accelerated"
    })

    # REMOVE EMPTY
    pie_df = pie_df.dropna()

    # =========================
    # SUMMARY
    # =========================
    summary = (
        pie_df["Programme Status"]
        .value_counts()
        .reset_index()
    )

    summary.columns = ["Status", "Count"]

    # =========================
    # COLORS
    # =========================
    color_map = {
        "On Track": "gold",
        "Delayed": "red",
        "Accelerated": "green"
    }

    # =========================
    # PIE
    # =========================
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
        paper_bgcolor="#1e1e2f",
        plot_bgcolor="#1e1e2f",
        font_color="white",
        height=420,
        margin=dict(t=60, b=20, l=20, r=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )