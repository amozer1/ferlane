import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def prepare(df):
    df = df.copy()

    df.columns = df.columns.astype(str).str.strip()

    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce").fillna(0)

    return df


def classify(row, today):
    if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
        return "On Track"

    if row["Finish"] < today and row["Activity % Complete"] < 100:
        return "Delayed"

    if row["Finish"] > today and row["Activity % Complete"] > 0:
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

    fig = go.Figure(
        data=[go.Pie(
            labels=summary.index,
            values=summary.values,
            hole=0,
            sort=False,
            textinfo="label+percent"
        )]
    )

    fig.update_layout(
        height=320,
        margin=dict(t=10, b=10, l=10, r=10),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)