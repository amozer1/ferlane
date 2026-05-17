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
    # CARD INTERNAL LAYOUT (LOCKED)
    # =========================
    with st.container():

        col1, col2 = st.columns([1.1, 1])

        # =========================
        # PIE (LEFT - INSIDE CARD)
        # =========================
        with col1:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        marker=dict(colors=colors),
                        textinfo="value+percent",
                        sort=False
                    )
                ]
            )

            fig.update_layout(
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="white",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

        # =========================
        # LEGEND (RIGHT SIDE)
        # =========================
        with col2:

            st.markdown("### Legend")

            st.markdown(f"""
            🟡 **On Track:** {on_track}  
            🔴 **Delayed:** {delayed}  
            🟢 **Accelerated:** {accelerated}
            """)