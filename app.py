import streamlit as st
import pandas as pd
from pathlib import Path

from utils.cleaner import clean_programme
from utils.comparison import compare_programmes
from utils.calculations import calculate_deltas
from utils.classifications import classify_activity

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Design Deliverable Tracker",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================

st.title("📊 Design Deliverable Tracker")
st.markdown("### NEC Clause 31 vs Clause 32 Programme Comparison")

# ======================================================
# FILE PATHS
# ======================================================

DATA_FOLDER = Path("data")

CL31_FILE = DATA_FOLDER / "CL31.csv"
CL32_FILE = DATA_FOLDER / "CL32.csv"

# ======================================================
# LOAD FILES
# ======================================================

try:

    df31 = pd.read_csv(CL31_FILE)
    df32 = pd.read_csv(CL32_FILE)

    # ==================================================
    # CLEAN DATA
    # ==================================================

    df31 = clean_programme(df31)
    df32 = clean_programme(df32)

    # ==================================================
    # COMPARE
    # ==================================================

    merged = compare_programmes(df31, df32)

    # ==================================================
    # CALCULATE DELTAS
    # ==================================================

    merged = calculate_deltas(merged)

    # ==================================================
    # CLASSIFY
    # ==================================================

    merged["Status"] = merged.apply(
        classify_activity,
        axis=1
    )

    # ==================================================
    # KPI SECTION
    # ==================================================

    total_activities = len(merged)

    delayed = len(
        merged[merged["Status"] == "Delayed"]
    )

    accelerated = len(
        merged[merged["Status"] == "Accelerated"]
    )

    on_track = len(
        merged[merged["Status"] == "On Track"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Activities",
        total_activities
    )

    col2.metric(
        "Delayed",
        delayed
    )

    col3.metric(
        "Accelerated",
        accelerated
    )

    col4.metric(
        "On Track",
        on_track
    )

    # ==================================================
    # STATUS FILTER
    # ==================================================

    status_filter = st.selectbox(
        "Filter Status",
        [
            "All",
            "Delayed",
            "Accelerated",
            "On Track",
            "New Activity",
            "Removed"
        ]
    )

    if status_filter != "All":

        merged = merged[
            merged["Status"] == status_filter
        ]

    # ==================================================
    # DISPLAY TABLE
    # ==================================================

    st.subheader("Programme Comparison")

    st.dataframe(
        merged[
            [
                "Activity ID",
                "Activity Name_31",
                "Start_31",
                "Finish_31",
                "Start_32",
                "Finish_32",
                "Delta Start Days",
                "Delta Finish Days",
                "Float Variance",
                "Status"
            ]
        ],
        use_container_width=True
    )

except Exception as e:

    st.error("Error processing programmes.")
    st.exception(e)