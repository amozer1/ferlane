import streamlit as st
import plotly.graph_objects as go


def render_pie(result):

    # =========================
    # COUNTS
    # =========================
    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    labels = ["On Track", "Delayed", "Accelerated"]
    values = [on_track, delayed, accelerated]

    colors = ["gold", "red", "green"]

    # =========================
    # PIE CHART
    # =========================
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textinfo="percent",
                sort=False
            )
        ]
    )

    fig.update_layout(
        height=220,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    # =========================
    # RENDER PIE
    # =========================
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # =========================
    # LEGEND (SAFE INSIDE STREAMLIT)
    # =========================
    st.markdown("**Legend**")

    c1, c2, c3 = st.columns(3)

    c1.metric("🟡 On Track", on_track)
    c2.metric("🔴 Delayed", delayed)
    c3.metric("🟢 Accelerated", accelerated)