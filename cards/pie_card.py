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
    # LAYOUT
    # =========================
    left, right = st.columns([1.3, 1])

    # =========================
    # PIE
    # =========================
    with left:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "On Track",
                        "Delayed",
                        "Accelerated"
                    ],
                    values=[
                        on_track,
                        delayed,
                        accelerated
                    ],
                    marker=dict(
                        colors=[
                            "gold",
                            "red",
                            "green"
                        ]
                    ),
                    textinfo="none",
                    sort=False
                )
            ]
        )

        fig.update_layout(
            autosize=False,
            width=260,
            height=260,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=False
        )

    # =========================
    # LEGEND
    # =========================
    with right:

        st.markdown(f"""
        <div style='padding-top:55px;'>

        <p style='color:gold; font-size:18px; font-weight:700;'>
        ● On Track: {on_track}
        </p>

        <p style='color:red; font-size:18px; font-weight:700;'>
        ● Delayed: {delayed}
        </p>

        <p style='color:limegreen; font-size:18px; font-weight:700;'>
        ● Accelerated: {accelerated}
        </p>

        </div>
        """, unsafe_allow_html=True)