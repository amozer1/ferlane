# app.py

import streamlit as st

from utils.loader import load_programme
from components.deliverables import extract_deliverables
from components.dashboard import build_dashboard_card

st.set_page_config(layout="wide")

st.title("📊 NEC Programme Comparison Dashboard (CL31 vs CL32)")

# -------------------------
# FILE UPLOAD
# -------------------------
cl31_file = st.file_uploader("Upload CL31 Excel", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32 Excel", type=["xlsx"])

# -------------------------
# RUN
# -------------------------
if cl31_file and cl32_file:

    cl31_df = load_programme(cl31_file)
    cl32_df = load_programme(cl32_file)

    # build dashboard
    dashboard = build_dashboard_card(cl31_df, cl32_df)

    st.subheader("Deliverables Performance Card")

    st.dataframe(
        dashboard,
        use_container_width=True
    )

else:
    st.info("Upload both CL31 and CL32 files to generate comparison")