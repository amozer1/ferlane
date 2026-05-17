import streamlit as st
import plotly.graph_objects as go


def render_pie(result):

    # =========================
    # COUNTS
    # =========================
    on_track = (result["Change Type"] == "UNCHANGED").sum()
    delayed = (result["Change Type"] == "DELAYED").sum()
    accelerated = (result["Change Type"] == "EARLY").sum()

    labels = [
        "On Track",
        "Delayed",
        "Accelerated"
    ]

    values = [
        on_track,
        delayed,
        accelerated
    ]

    colors = [
        "gold",
        "red",
        "green"
    ]

    # =========================
    # CARD LAYOUT
    # =========================
    left, right = st.columns([1.2, 1])

    # =========================
    # PIE
    # =========================
    with left:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0,
                    marker=dict(colors=colors),
                    textinfo="percent+value",
                    textfont_size=14,
                    insidetextorientation="radial",
                    sort=False
                )
            ]
        )

        fig.update_layout(
            autosize=False,
            width=250,
            height=250,
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0
            ),
            paper_bgcolor="white",
            plot_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(
            fig,
            use_container_width=False,
            config={
                "displayModeBar": False
            }
        )

    # =========================
    # LEGEND
    # =========================
    with right:

        st.markdown(f"""
        <div style="
            padding-top:45px;
            padding-left:10px;
        ">

        <div style="
            color:gold;
            font-size:18px;
            font-weight:700;
            margin-bottom:18px;
        ">
        ● On Track: {on_track}
        </div>

        <div style="
            color:red;
            font-size:18px;
            font-weight:700;
            margin-bottom:18px;
        ">
        ● Delayed: {delayed}
        </div>

        <div style="
            color:limegreen;
            font-size:18px;
            font-weight:700;
        ">
        ● Accelerated: {accelerated}
        </div>

        </div>
        """, unsafe_allow_html=True)