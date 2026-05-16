import streamlit as st
from utils.loader import load_programme
from components.deliverables import build_deliverables_card

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="CL31 vs CL32 Deliverables Tracker",
    layout="wide"
)

st.title("📊 CL31 vs CL32 Programme Deliverables Tracker")

# ----------------------------
# LOAD DATA
# ----------------------------
cl31_file = "data/CL31.xlsx"
cl32_file = "data/CL32.xlsx"

cl31_df = load_programme(cl31_file)
cl32_df = load_programme(cl32_file)

# ----------------------------
# VALIDATION
# ----------------------------
if cl31_df is None or cl32_df is None:
    st.error("Failed to load programme data. Check Excel files and loader.")
    st.stop()

# ----------------------------
# BUILD DELIVERABLE CARD
# ----------------------------
card_df = build_deliverables_card(cl31_df, cl32_df)

# ----------------------------
# DISPLAY (SINGLE CARD ONLY)
# ----------------------------
st.subheader("📌 Deliverables Comparison (CL31 vs CL32)")

st.dataframe(
    card_df,
    use_container_width=True,
    hide_index=True
)