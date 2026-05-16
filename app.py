# app.py

import streamlit as st
import pandas as pd

from utils.loader import load_programme
from components.deliverables import extract_deliverables

st.set_page_config(layout="wide")

st.title("📊 CL31 vs CL32 Deliverables Dashboard")

# -------------------------
# FILE UPLOAD
# -------------------------
cl31_file = st.file_uploader("Upload CL31 Excel", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32 Excel", type=["xlsx"])

# -------------------------
# MAIN LOGIC
# -------------------------
if cl31_file and cl32_file:

    cl31_df = load_programme(cl31_file)
    cl32_df = load_programme(cl32_file)

    cl31_del = extract_deliverables(cl31_df)
    cl32_del = extract_deliverables(cl32_df)

    # convert to frames
    df31 = pd.DataFrame({"Deliverable": cl31_del})
    df32 = pd.DataFrame({"Deliverable": cl32_del})

    # merge comparison
    merged = pd.merge(
        df31,
        df32,
        on="Deliverable",
        how="outer",
        indicator=True
    )

    # status logic
    def status(x):
        if x == "both":
            return "🟢 Both CL31 & CL32"
        elif x == "left_only":
            return "🔵 CL31 Only"
        else:
            return "🟣 CL32 Only"

    merged["Status"] = merged["_merge"].apply(status)

    st.subheader("Deliverables Comparison")

    st.dataframe(
        merged[["Deliverable", "Status"]],
        use_container_width=True
    )

else:
    st.info("Upload CL31 and CL32 Excel files to begin")