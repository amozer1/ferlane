import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def prepare(df):
    df = df.copy()

    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["Activity % Complete"] = pd.to_numeric(
        df["Activity % Complete"],
        errors="coerce"
    ).fillna(0)

    return df


def classify(row, today):
    start = row["Start"]
    finish = row["Finish"]
    pct = row["Activity % Complete"]

    if pd.isna(start) or pd.isna(finish):
        return "On Track"

    if finish < today and pct < 100:
        return "Delayed"

    if finish > today and pct > 0:
        return "Accelerated"

    return "On Track"


def render_pie(df):
    df = prepare(df)
    today = pd.Timestamp.today()

    df["Status"] = df.apply(lambda r: classify(r, today), axis=1)

    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    labels = ["On Track", "Delayed", "Accelerated"]
    values = [
        summary["On Track"],
        summary["Delayed"],
        summary["Accelerated"]
    ]

    colors = ["#FFD700", "#FF4B4B", "#00C853"]

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo="label+percent",
            hole=0,
            sort=False
        )]
    )

    fig.update_layout(
        title=None,
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, b=10, l=10, r=10),
        height=280
    )

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Legend")

        st.markdown(f"🟡 On Track: {summary['On Track']}")
        st.markdown(f"🔴 Delayed: {summary['Delayed']}")
        st.markdown(f"🟢 Accelerated: {summary['Accelerated']}")