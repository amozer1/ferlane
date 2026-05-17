import streamlit as st
import plotly.graph_objects as go


def render_pie(result):

    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=["On Track", "Delayed", "Accelerated"],
                values=[on_track, delayed, accelerated],
                marker=dict(colors=["gold", "red", "green"]),
                textinfo="percent",
                sort=False
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False,
        height=260
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Legend")
    st.write(f"🟡 On Track: {on_track}")
    st.write(f"🔴 Delayed: {delayed}")
    st.write(f"🟢 Accelerated: {accelerated}")