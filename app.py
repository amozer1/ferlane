import streamlit as st
import pandas as pd

from utils.loader import load_cl31, load_cl32
from components.deliverables import build_deliverables_report

st.set_page_config(layout="wide")

st.title("Deliverables Comparison (CL31 vs CL32)")

cl31 = load_cl31()
cl32 = load_cl32()

df = build_deliverables_report(cl31, cl32)

# -----------------------------
# COLOUR LOGIC (UPDATED)
# -----------------------------
def status_color(val):
    if val == "DELAYED":
        return "background-color: #ffcccc"
    if val == "AHEAD":
        return "background-color: #cce5ff"
    if val == "UNCHANGED":
        return "background-color: #e6ffe6"
    if val == "NEW":
        return "background-color: #fff3cd"
    if val == "REMOVED":
        return "background-color: #d6d6d6"
    return ""

def delta_color(val):
    if pd.isna(val):
        return ""
    if val > 0:
        return "color: red; font-weight: bold"
    if val < 0:
        return "color: green; font-weight: bold"
    return ""

# -----------------------------
# STYLER (FIXED)
# -----------------------------
styled_df = (
    df.style
    .map(status_color, subset=["Status"])
    .map(delta_color, subset=["Delta (Days)"])
    .set_properties(**{
        "text-align": "left",
        "font-size": "14px"
    })
)

st.dataframe(styled_df, use_container_width=True)