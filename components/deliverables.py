import pandas as pd
import streamlit as st


def format_date(x):
    if pd.isna(x):
        return ""
    return pd.to_datetime(x).strftime("%d-%b-%y")


def build_status(delta):
    if pd.isna(delta):
        return "No data"
    if delta == 0:
        return "Stable"
    if delta > 30:
        return "Major delay"
    if delta > 0:
        return "Delayed"
    return "Ahead"


def render_deliverables_table(df):

    df = df.copy()

    df["CL31 Finish"] = df["CL31 Finish"].apply(format_date)
    df["CL32 Finish"] = df["CL32 Finish"].apply(format_date)

    df["Status / Comment"] = df["Delta (Days)"].apply(build_status)

    df = df.rename(columns={
        "Delta (Days)": "Delta (Days)"
    })

    st.dataframe(
        df[[
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Status / Comment"
        ]],
        use_container_width=True
    )