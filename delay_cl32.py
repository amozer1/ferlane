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


def get_delayed(df):
    df = prepare(df)
    today = pd.Timestamp.today()

    delayed = df[
        (df["Finish"] < today) &
        (df["Activity % Complete"] < 100)
    ].copy()

    delayed["Delay (Days)"] = (today - delayed["Finish"]).dt.days

    delayed = delayed[
        [
            "Activity ID",
            "Activity Name",
            "Start",
            "Finish",
            "Delay (Days)",
            "Comments"
        ]
    ].sort_values("Delay (Days)", ascending=False)

    return delayed


def render_delayed_table(df):
    import streamlit as st

    st.markdown("### 🔴 Delayed Deliverables (CL32)")

    delayed = get_delayed(df)

    st.dataframe(
        delayed,
        use_container_width=True,
        hide_index=True
    )