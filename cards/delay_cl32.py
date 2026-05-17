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

    df["Activity % Complete"] = pd.to_numeric(
        df["Activity % Complete"],
        errors="coerce"
    ).fillna(0)

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

    display_df = delayed[[
        "Activity ID",
        "Activity Name",
        "Start",
        "Finish",
        "Delay (Days)",
        "Comments"
    ]].copy()

    # Format dates ONLY for display (no data change)
    display_df["Start"] = display_df["Start"].dt.strftime("%d-%b-%Y")
    display_df["Finish"] = display_df["Finish"].dt.strftime("%d-%b-%Y")

    # =========================
    # VISUAL FORMATTING ONLY
    # =========================
    styled = display_df.style.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#140021"),
                ("color", "white"),
                ("font-size", "13px"),
                ("font-weight", "bold"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "1px"),
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

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True
    )