import streamlit as st
import pandas as pd


def _prepare(df):
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


def _get_delayed(df):
    df = _prepare(df)
    today = pd.Timestamp.today()

    delayed = df[
        (df["Finish"] < today) &
        (df["Activity % Complete"] < 100)
    ].copy()

    delayed["Delay (Days)"] = (today - delayed["Finish"]).dt.days

    return delayed.sort_values("Delay (Days)", ascending=False)


def render_delayed_table(df):
    delayed = _get_delayed(df)

    if delayed.empty:
        st.success("No delayed activities 🎯")
        return

    st.dataframe(
        delayed[[
            "Activity ID",
            "Activity Name",
            "Start",
            "Finish",
            "Delay (Days)",
            "Comments"
        ]],
        use_container_width=True,
        hide_index=True
    )