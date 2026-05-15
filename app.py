import streamlit as st
import pandas as pd
from pathlib import Path

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
st.markdown("### NEC Clause 31 vs Clause 32 Dashboard")

# ======================================================
# DATA PATHS
# ======================================================

DATA_FOLDER = Path("data")

CL31_FILE = DATA_FOLDER / "CL31.xlsx"
CL32_FILE = DATA_FOLDER / "CL32.xlsx"

# ======================================================
# LOAD FILES AUTOMATICALLY
# ======================================================

try:

    df31 = pd.read_excel(CL31_FILE)
    df32 = pd.read_excel(CL32_FILE)

    st.success("Programme files loaded successfully.")

    # ==================================================
    # KPI ROW
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "CL31 Activities",
        len(df31)
    )

    col2.metric(
        "CL32 Activities",
        len(df32)
    )

    col3.metric(
        "CL31 Columns",
        len(df31.columns)
    )

    col4.metric(
        "CL32 Columns",
        len(df32.columns)
    )

    # ==================================================
    # TABS
    # ==================================================

    tab1, tab2 = st.tabs([
        "Clause 31 Programme",
        "Clause 32 Programme"
    ])

    with tab1:
        st.dataframe(df31)

    with tab2:
        st.dataframe(df32)

except Exception as e:

    st.error("Programme files could not be loaded.")
    st.exception(e)