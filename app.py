# app.py

import streamlit as st
import pandas as pd
import numpy as np

from loader import load_cl31, load_cl32
from deliverables import build_deliverables


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="CL31 vs CL32 Deliverables",
    layout="wide"
)

st.title("📊 CL31 vs CL32 Deliverable Comparison")


# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

cl31 = load_cl31("data/CL31-February.xlsx")
cl32 = load_cl32("data/CL32-May.xlsx")

df = build_deliverables(cl31, cl32)


# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("Filters")

change_types = st.sidebar.multiselect(
    "Change Type",
    options=sorted(df["Change Type"].dropna().unique()),
    default=sorted(df["Change Type"].dropna().unique())
)

search = st.sidebar.text_input(
    "Search Deliverable"
)

float_filter = st.sidebar.selectbox(
    "Float Status",
    [
        "All",
        "Critical (<0)",
        "Near Critical (0-10)",
        "Healthy (>10)"
    ]
)


# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered = df.copy()

filtered = filtered[
    filtered["Change Type"].isin(change_types)
]

if search:
    filtered = filtered[
        filtered["Deliverable"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if float_filter == "Critical (<0)":
    filtered = filtered[filtered["Float"] < 0]

elif float_filter == "Near Critical (0-10)":
    filtered = filtered[
        (filtered["Float"] >= 0) &
        (filtered["Float"] <= 10)
    ]

elif float_filter == "Healthy (>10)":
    filtered = filtered[filtered["Float"] > 10]


# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

st.subheader("Programme Summary")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Deliverables",
    len(df)
)

c2.metric(
    "Delayed",
    (df["Change Type"] == "DELAYED").sum()
)

c3.metric(
    "Early",
    (df["Change Type"] == "EARLY").sum()
)

c4.metric(
    "New",
    (df["Change Type"] == "NEW").sum()
)

c5.metric(
    "Removed",
    (df["Change Type"] == "REMOVED").sum()
)


# ---------------------------------------------------
# TABLE STYLING
# ---------------------------------------------------

def row_colour(row):

    change = row["Change Type"]

    if change == "DELAYED":
        return ["background-color: #ffdddd"] * len(row)

    elif change == "EARLY":
        return ["background-color: #ddffdd"] * len(row)

    elif change == "NEW":
        return ["background-color: #ddeeff"] * len(row)

    elif change == "REMOVED":
        return ["background-color: #eeeeee"] * len(row)

    elif change == "UNCHANGED":
        return ["background-color: #fff8d6"] * len(row)

    return [""] * len(row)


def delta_colour(val):

    if pd.isna(val):
        return ""

    if val > 0:
        return "color: red; font-weight: bold"

    elif val < 0:
        return "color: green; font-weight: bold"

    return "color: grey"


def float_colour(val):

    if pd.isna(val):
        return ""

    if val < 0:
        return "color: red; font-weight: bold"

    elif val <= 10:
        return "color: orange; font-weight: bold"

    return "color: green; font-weight: bold"


styled = (
    filtered.style
    .apply(row_colour, axis=1)
    .map(delta_colour, subset=["Delta (Days)"])
    .map(float_colour, subset=["Float"])
)


# ---------------------------------------------------
# TABLE
# ---------------------------------------------------

st.subheader("Deliverables Comparison")

st.dataframe(
    styled,
    use_container_width=True,
    height=700
)


# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="deliverable_comparison.csv",
    mime="text/csv"
)