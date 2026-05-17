import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def render_pie(df):

    st.markdown("### Schedule Summary (CL32)")

    df = df.copy()

    # =========================
    # CLEAN COLUMN HEADERS
    # =========================
    df.columns = df.columns.astype(str).str.strip()

    # =========================
    # SAFETY CHECK
    # =========================
    required = ["Start", "Finish", "Activity % Complete"]

    for col in required:
        if col not in df.columns:
            st.error(f"Missing column: {col}")
            st.write(df.columns.tolist())
            return

    # =========================
    # PARSE DATES
    # =========================
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # =========================
    # CLEAN % COMPLETE
    # =========================
    def parse_pct(x):
        try:
            return float(str(x).replace("%", "").strip())
        except:
            return 0

    df["Progress"] = df["Activity % Complete"].apply(parse_pct)

    today = pd.to_datetime(datetime.today().date())

    # =========================
    # CLASSIFICATION LOGIC
    # =========================
    def status(row):

        if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
            return "On Track"

        duration = (row["Finish"] - row["Start"]).days
        if duration <= 0:
            return "On Track"

        elapsed = (today - row["Start"]).days
        expected = max(min(elapsed / duration, 1), 0)

        actual = row["Progress"] / 100

        diff = actual - expected

        if diff < -0.1:
            return "Delayed"
        elif diff > 0.1:
            return "Accelerated"
        else:
            return "On Track"

    df["Status"] = df.apply(status, axis=1)

    # =========================
    # FORCE ALL 3 CATEGORIES
    # =========================
    summary = df["Status"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]

    for s in ["On Track", "Delayed", "Accelerated"]:
        if s not in summary["Status"].values:
            summary = pd.concat(
                [summary, pd.DataFrame([[s, 0]], columns=["Status", "Count"])],
                ignore_index=True
            )

    # =========================
    # COLORS
    # =========================
    color_map = {
        "On Track": "gold",
        "Delayed": "red",
        "Accelerated": "green"
    }

    # =========================
    # PIE (FULL, THICK, NO DONUT)
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
        pull=[0.02, 0.02, 0.02],
        marker=dict(line=dict(color="white", width=2))
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=380,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)