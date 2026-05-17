import streamlit as st
import plotly.express as px
import pandas as pd


def render_pie(result):

    # =========================
    # COUNTS
    # =========================
    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    summary = pd.DataFrame({
        "Status": ["On Track", "Delayed", "Accelerated"],
        "Count": [on_track, delayed, accelerated]
    })

    # =========================
    # PIE
    # =========================
    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map={
            "On Track": "gold",
            "Delayed": "red",
            "Accelerated": "green"
        }
    )

    # =========================
    # MAKE PIE THICK + FIT CARD
    # =========================
    fig.update_traces(
        textinfo="none",
        sort=False
    )

    fig.update_layout(
        height=220,
        margin=dict(t=5, b=5, l=5, r=5),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )
    # =========================
    # LAYOUT
    # =========================
    left, right = st.columns([2, 1])

    with left:
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown("""
        <div style='padding-top:30px;'>

        <p style='color:gold; font-size:16px; font-weight:600;'>
        ● On Track: {}
        </p>

        <p style='color:red; font-size:16px; font-weight:600;'>
        ● Delayed: {}
        </p>

        <p style='color:limegreen; font-size:16px; font-weight:600;'>
        ● Accelerated: {}
        </p>

        </div>
        """.format(
            on_track,
            delayed,
            accelerated
        ), unsafe_allow_html=True)