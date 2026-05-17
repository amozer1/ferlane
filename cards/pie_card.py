import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime


def render_pie(df):

    st.markdown("### Schedule Summary (CL32)")

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce").fillna(0)

    today = pd.to_datetime(datetime.today().date())

    # =========================
    # EXPECTED PROGRESS
    # =========================
    duration = (df["Finish"] - df["Start"]).dt.days
    elapsed = (today - df["Start"]).dt.days

    df["Expected"] = (elapsed / duration) * 100
    df["Expected"] = df["Expected"].fillna(0)

    # =========================
    # CLASSIFICATION LOGIC
    # =========================
    def classify(row):
        if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
            return None

        if row["Activity % Complete"] >= row["Expected"] + 5:
            return "Accelerated"
        elif row["Activity % Complete"] <= row["Expected"] - 5:
            return "Delayed"
        else:
            return "On Track"

    df["Status"] = df.apply(classify, axis=1)
    df = df[df["Status"].notna()]

    # =========================
    # SUMMARY (INCLUDES ZEROS)
    # =========================
    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    ).reset_index()

    summary.columns = ["Status", "Count"]

    # =========================
    # COLORS
    # =========================
    color_map = {
        "On Track": "gold",
        "Delayed": "red",
        "Accelerated": "green"
    }

    # =========================
    # FIXED SIZE PIE (IMPORTANT)
    # =========================
    fig = px.pie(
        summary,
        names="Status",
        values="Count",
        color="Status",
        color_discrete_map=color_map,
        hole=0  # 🔥 THICK PIE (NOT DONUT BORDER EFFECT)
    )

    fig.update_layout(
        height=320,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    # =========================
    # LEGEND INSIDE CARD (MANUAL)
    # =========================
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        **Legend**

        🟡 On Track: {0}  
        🔴 Delayed: {1}  
        🟢 Accelerated: {2}
        """.format(
            int(summary[summary["Status"]=="On Track"]["Count"].values[0]),
            int(summary[summary["Status"]=="Delayed"]["Count"].values[0]),
            int(summary[summary["Status"]=="Accelerated"]["Count"].values[0]),
        ))