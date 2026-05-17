import streamlit as st
import pandas as pd
import numpy as np


# =========================
# DATA PREPARATION
# =========================
def _prepare(df):
    df = df.copy()

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Convert dates
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # Clean % complete
    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["Activity % Complete"] = (
        pd.to_numeric(df["Activity % Complete"], errors="coerce")
        .fillna(0)
    )

    return df


# =========================
# DELAY LOGIC
# =========================
def _get_delayed(df):
    df = _prepare(df)
    today = pd.Timestamp.today()

    delayed = df[
        (df["Finish"] < today) &
        (df["Activity % Complete"] < 100)
    ].copy()

    delayed["Delay (Days)"] = (today - delayed["Finish"]).dt.days

    # Severity bands
    delayed["Severity"] = pd.cut(
        delayed["Delay (Days)"],
        bins=[-1, 7, 30, 90, np.inf],
        labels=["🟡 Low", "🟠 Medium", "🔴 High", "⚫ Critical"]
    )

    return delayed.sort_values("Delay (Days)", ascending=False)


# =========================
# TABLE RENDERER
# =========================
def render_delayed_table(df):
    delayed = _get_delayed(df)

    if delayed.empty:
        st.success("No delayed activities 🎯")
        return

    display_df = delayed[[
        "Activity ID",
        "Activity Name",
        "Start",
        "Finish",
        "Delay (Days)",
        "Severity",
        "Activity % Complete",
        "Comments"
    ]].copy()

    # Format dates
    display_df["Start"] = display_df["Start"].dt.strftime("%d-%b-%Y")
    display_df["Finish"] = display_df["Finish"].dt.strftime("%d-%b-%Y")

    # Format %
    display_df["Activity % Complete"] = (
        display_df["Activity % Complete"].round(1).astype(str) + "%"
    )

    # =========================
    # STYLING (DASHBOARD LOOK)
    # =========================
    styled = display_df.style

    # Header styling (IMPORTANT VISUAL UPGRADE)
    styled = styled.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#140021"),
                ("color", "white"),
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "1.2px"),
                ("padding", "10px"),
                ("border-bottom", "3px solid #ffcc00"),
                ("text-align", "left")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("padding", "8px"),
                ("background-color", "#1e0033"),
                ("color", "white"),
                ("border-bottom", "1px solid #2d004d")
            ]
        },
        {
            "selector": "table",
            "props": [
                ("border-collapse", "collapse"),
                ("width", "100%")
            ]
        }
    ])

    # Severity colour coding
    def highlight_severity(val):
        if "Critical" in str(val):
            return "background-color:#5a0000; color:white; font-weight:bold"
        elif "High" in str(val):
            return "background-color:#8b1e1e; color:white; font-weight:bold"
        elif "Medium" in str(val):
            return "background-color:#a66a00; color:white; font-weight:bold"
        elif "Low" in str(val):
            return "background-color:#4a4a00; color:white; font-weight:bold"
        return ""

    styled = styled.applymap(
        highlight_severity,
        subset=["Severity"]
    )

    # =========================
    # RENDER
    # =========================
    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True
    )