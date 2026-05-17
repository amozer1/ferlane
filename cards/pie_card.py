import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def render_pie(df):

    st.markdown("### Schedule Summary (CL32)")

    # =========================
    # CLEAN DATA
    # =========================
    df = df.copy()

    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # Convert % Complete safely
    def parse_pct(x):
        try:
            return float(str(x).replace("%", ""))
        except:
            return 0

    df["Progress"] = df["Activity % Complete"].apply(parse_pct)

    today = pd.to_datetime(datetime.today().date())

    # =========================
    # STATUS CALCULATION
    # =========================
    def classify(row):
        if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
            return "On Track"

        total_days = (row["Finish"] - row["Start"]).days
        elapsed = (today - row["Start"]).days

        if total_days <= 0:
            return "On Track"

        time_progress = max(min(elapsed / total_days, 1), 0)
        actual_progress = row["Progress"] / 100

        diff = actual_progress - time_progress

        if diff < -0.1:
            return "Delayed"
        elif diff > 0.1:
            return "Accelerated"
        else:
            return "On Track"

    df["Programme Status"] = df.apply(classify, axis=1)

    # =========================
    # SUMMARY
    # =========================
    summary = df["Programme Status"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]

    # ensure all exist even if zero
    for s in ["On Track", "Delayed", "Accelerated"]:
        if s not in summary["Status"].values:
            summary = pd.concat([
                summary,
                pd.DataFrame([{"Status": s, "Count": 0}])
            ])

    # =========================
    # COLORS
    # =========================
    color_map = {
        "On Track": "gold",
        "Delayed": "red",
        "Accelerated": "green"
    }

    # =========================
    # PIE (THICK PIE - NOT DONUT)
    # =========================
    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map=color_map
    )

    fig.update_traces(
        textinfo="label+value+percent",
        hole=0  # IMPORTANT → solid pie
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=10, b=10, l=10, r=10),
        height=380
    )

    st.plotly_chart(fig, use_container_width=True)