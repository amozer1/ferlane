# app.py

import streamlit as st
import pandas as pd

from loader import load_schedule
from deliverables import build_comparison_table

st.set_page_config(
    page_title="FERLANE Deliverables Tracker",
    layout="wide"
)

st.title("FERLANE Design Deliverables Tracker")

# =========================
# LOAD DATA
# =========================

cl31 = load_schedule("data/CL31-February.xlsx")
cl32 = load_schedule("data/CL32-May.xlsx")

comparison_df = build_comparison_table(cl31, cl32)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

discipline_filter = st.sidebar.multiselect(
    "Discipline",
    sorted(comparison_df["Discipline"].dropna().unique()),
    default=sorted(comparison_df["Discipline"].dropna().unique())
)

change_filter = st.sidebar.multiselect(
    "Change Type",
    sorted(comparison_df["Change Type"].dropna().unique()),
    default=sorted(comparison_df["Change Type"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Float Status",
    sorted(comparison_df["Float Status"].dropna().unique()),
    default=sorted(comparison_df["Float Status"].dropna().unique())
)

search = st.sidebar.text_input("Search Deliverable")

# =========================
# FILTER DATA
# =========================

filtered_df = comparison_df[
    comparison_df["Discipline"].isin(discipline_filter)
]

filtered_df = filtered_df[
    filtered_df["Change Type"].isin(change_filter)
]

filtered_df = filtered_df[
    filtered_df["Float Status"].isin(status_filter)
]

if search:
    filtered_df = filtered_df[
        filtered_df["Deliverable"]
        .str.contains(search, case=False, na=False)
    ]

# =========================
# METRICS
# =========================

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Deliverables",
    len(filtered_df)
)

col2.metric(
    "Delayed",
    len(filtered_df[filtered_df["Change Type"] == "DELAYED"])
)

col3.metric(
    "Accelerated",
    len(filtered_df[filtered_df["Change Type"] == "ACCELERATED"])
)

col4.metric(
    "Critical",
    len(filtered_df[filtered_df["Float Status"] == "Critical"])
)

col5.metric(
    "New",
    len(filtered_df[filtered_df["Change Type"] == "NEW"])
)

# =========================
# TABLE STYLING
# =========================

def row_colour(row):

    if row["Change Type"] == "DELAYED":
        return ["background-color: #ffcccc"] * len(row)

    elif row["Change Type"] == "ACCELERATED":
        return ["background-color: #ccffcc"] * len(row)

    elif row["Change Type"] == "NEW":
        return ["background-color: #cce5ff"] * len(row)

    elif row["Change Type"] == "REMOVED":
        return ["background-color: #ffe0b3"] * len(row)

    return [""] * len(row)

styled_df = (
    filtered_df
    .style
    .apply(row_colour, axis=1)
)

# =========================
# DISPLAY TABLE
# =========================

st.subheader("Deliverables Comparison Register")

st.dataframe(
    styled_df,
    use_container_width=True,
    height=750
)