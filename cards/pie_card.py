import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def render_pie(df):

    df = df.copy()

    # clean column names
    df.columns = df.columns.astype(str).str.strip()

    # required CL32 columns only
    required_cols = ["Start", "Finish", "Activity % Complete"]

    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing column in CL32: {col}")
            st.write(df.columns.tolist())
            return

    # parse dates
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # convert % complete safely
    def to_pct(x):
        try:
            return float(str(x).replace("%", "").strip())
        except:
            return 0

    df["progress"] = df["Activity % Complete"].apply(to_pct)

    today = pd.to_datetime(datetime.today().date())

    # =========================
    # STATUS LOGIC
    # =========================
    def get_status(row):

        if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
            return "On Track"

        duration = (row["Finish"] - row["Start"]).days
        if duration <= 0:
            return "On Track"

        elapsed = (today - row["Start"]).days
        expected = max(min(elapsed / duration, 1), 0)

        actual = row["progress"] / 100

        diff = actual - expected

        if diff < -0.1:
            return "Delayed"
        elif diff > 0.1:
            return "Accelerated"
        else:
            return "On Track"

    df["Status"] = df.apply(get_status, axis=1)

    # =========================
    # SUMMARY
    # =========================
    summary = df["Status"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]

    # ensure all categories exist
    for s in ["On Track", "Delayed", "Accelerated"]:
        if s not in summary["Status"].values:
            summary = pd.concat(
                [summary, pd.DataFrame([[s, 0]], columns=["Status", "Count"])],
                ignore_index=True
            )

    # remove zeros from pie (clean view)
    summary = summary[summary["Count"] > 0]

    if summary.empty:
        summary = pd.DataFrame({"Status": ["On Track"], "Count": [1]})

    # =========================
    # PIE CHART (THICK PIE, NO DONUT)
    # =========================
    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map={
            "On Track": "gold",
            "Delayed": "red",
            "Accelerated": "green"
        }
    )

    fig.update_traces(
        textinfo="label+percent",
        hole=0,  # FULL PIE (NOT DONUT)
        pull=[0.02] * len(summary)
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=5, r=5, t=5, b=5),
        height=320,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)