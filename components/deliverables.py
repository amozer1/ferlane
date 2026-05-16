import pandas as pd
import streamlit as st


def format_date(x):
    if pd.isna(x):
        return "—"
    return pd.to_datetime(x).strftime("%d-%b-%y")


def status_comment(row):

    if row["Change Type"] == "NEW":
        return "Added scope in CL32"

    if row["Change Type"] == "REMOVED":
        return "Dropped from CL32"

    if row["Change Type"] == "UNCHANGED":
        return "Stable"

    if row["Change Type"] == "DELAYED":
        if row["Delta (Days)"] > 30:
            return "Major delay – critical attention required"
        return "Minor slip – coordination required"

    if row["Change Type"] == "ACCELERATED":
        return "Programme improvement"

    return "Review required"


def render_table(df):

    df = df.copy()

    df["CL31 Finish"] = df["CL31 Finish"].apply(format_date)
    df["CL32 Finish"] = df["CL32 Finish"].apply(format_date)

    df["Delta (Days)"] = df["Delta (Days)"].apply(
        lambda x: "—" if pd.isna(x) else f"{int(x):+d}"
    )

    df["Status / Comment"] = df.apply(status_comment, axis=1)

    final = df[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    st.dataframe(final, use_container_width=True)