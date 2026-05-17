import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def classify(df):
    df = df.copy()

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce").fillna(0)

    def status(x):
        if x >= 100:
            return "On Track"
        elif x >= 50:
            return "Delayed"
        else:
            return "Accelerated"

    df["Status"] = df["Activity % Complete"].apply(status)

    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    return summary


def render_pie(df):

    summary = classify(df)

    labels = ["On Track", "Delayed", "Accelerated"]
    values = [
        summary["On Track"],
        summary["Delayed"],
        summary["Accelerated"]
    ]

    colors = ["#FFD700", "#FF4B4B", "#00C853"]

    total = sum(values)

    # avoid empty crash
    if total == 0:
        values = [1, 0, 0]
        total = 1

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hole=0,  # full pie
                sort=False,
                hoverinfo="label+value"
            )
        ]
    )

    # central label (BIG UPGRADE LOOK)
    fig.update_layout(
        annotations=[
            dict(
                text=f"Total<br><b>{total}</b>",
                x=0.5,
                y=0.5,
                font_size=18,
                showarrow=False
            )
        ],
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10),
        height=320
    )

    # layout split: pie + legend
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Legend")

        st.markdown(f"🟡 On Track: **{summary['On Track']}**")
        st.markdown(f"🔴 Delayed: **{summary['Delayed']}**")
        st.markdown(f"🟢 Accelerated: **{summary['Accelerated']}**")