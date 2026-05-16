import streamlit as st
import pandas as pd

from utils.loader import load_programme
from components.deliverables import extract_deliverables, build_deliverables_card


st.set_page_config(layout="wide")

st.title("Deliverable Tracker Dashboard")


# -------------------------
# FILE LOADERS
# -------------------------
cl31_file = st.file_uploader("Upload CL31", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32", type=["xlsx"])


if cl31_file and cl32_file:

    cl31_df = load_programme(cl31_file)
    cl32_df = load_programme(cl32_file)

    # -------------------------
    # COMBINE
    # -------------------------
    df = pd.concat([cl31_df, cl32_df], ignore_index=True)

    # -------------------------
    # EXTRACT DELIVERABLES
    # -------------------------
    deliverables_df = extract_deliverables(df)

    final_df = build_deliverables_card(deliverables_df)

    # -------------------------
    # DISPLAY SINGLE CARD TABLE
    # -------------------------
    st.subheader("Schedule Summary")

    st.dataframe(
        final_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Upload both CL31 and CL32 files to continue.")