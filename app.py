import streamlit as st
import pandas as pd

from loader import load_schedule
from deliverables import build_deliverables


st.set_page_config(layout="wide")

st.title("📊 Deliverable Tracker (CL31 vs CL32)")


# ---------- FILE INPUTS ----------
cl31_file = st.file_uploader("Upload CL31 Excel", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32 Excel", type=["xlsx"])


if cl31_file and cl32_file:

    df31 = load_schedule(cl31_file)
    df32 = load_schedule(cl32_file)

    # ---------- ALIGN DATA ----------
    # Merge on Activity Name (your requirement)
    merged = pd.merge(
        df31,
        df32,
        on="Activity Name",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # Rebuild clean structure
    clean = pd.DataFrame()
    clean["Activity Name"] = merged["Activity Name"]

    clean["BL1 Finish"] = merged.get("BL1 Finish_CL31")
    clean["Finish"] = merged.get("Finish_CL32")

    # ---------- BUILD DELIVERABLE TABLE ----------
    result = build_deliverables(clean)

    # ---------- SIDEBAR FILTERS ----------
    st.sidebar.header("Filters")

    status_filter = st.sidebar.multiselect(
        "Change Type",
        options=result["Change Type"].unique(),
        default=result["Change Type"].unique()
    )

    filtered = result[result["Change Type"].isin(status_filter)]

    # ---------- MAIN TABLE ----------
    st.subheader("Deliverables Comparison Table")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Upload both CL31 and CL32 files to generate tracker.")