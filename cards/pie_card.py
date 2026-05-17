import streamlit as st
import plotly.graph_objects as go


def render_pie(result):

    # =========================
    # DATA
    # =========================
    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    labels = ["On Track", "Delayed", "Accelerated"]
    values = [on_track, delayed, accelerated]
    colors = ["gold", "red", "green"]

    # =========================
    # CARD WRAPPER (STRICT CONTAINER)
    # =========================
    with st.container():

        col1, col2 = st.columns([1, 1])

        # =========================
        # PIE (LEFT)
        # =========================
        with col1:

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=labels,
                        values=values,
                        marker=dict(colors=colors),
                        textinfo="value+percent",
                        sort=False,
                        hole=0  # solid pie (NOT donut)
                    )
                ]
            )

            fig.update_layout(
                height=260,
                margin=dict(l=0, r=0, t=0, b=0),  # 🔥 removes overflow
                paper_bgcolor="white",
                plot_bgcolor="white",
                showlegend=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False}
            )

        # =========================
        # LEGEND (RIGHT)
        # =========================
        with col2:

            st.markdown("### Legend")

            st.markdown(f"""
            🟡 **On Track:** {on_track}  
            🔴 **Delayed:** {delayed}  
            🟢 **Accelerated:** {accelerated}
            """)