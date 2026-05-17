import streamlit as st
import plotly.graph_objects as go


def render_pie(result):

    # =========================
    # COUNTS
    # =========================
    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    # =========================
    # FILTER OUT ZERO VALUES
    # =========================
    labels = []
    values = []
    colors = []

    if on_track > 0:
        labels.append("On Track")
        values.append(on_track)
        colors.append("gold")

    if delayed > 0:
        labels.append("Delayed")
        values.append(delayed)
        colors.append("red")

    if accelerated > 0:
        labels.append("Accelerated")
        values.append(accelerated)
        colors.append("green")

    # =========================
    # PIE + LEGEND LAYOUT
    # =========================
    col1, col2 = st.columns([1.2, 1])

    with col1:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),

                    # SHOW VALUE + %
                    textinfo="value+percent",
                    textfont_size=14,
                    sort=False
                )
            ]
        )

        fig.update_layout(
            width=320,
            height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=False)

    with col2:

        st.markdown("### Legend")

        if on_track > 0:
            st.markdown(f"🟡 **On Track:** {on_track}")

        if delayed > 0:
            st.markdown(f"🔴 **Delayed:** {delayed}")

        if accelerated > 0:
            st.markdown(f"🟢 **Accelerated:** {accelerated}")