import streamlit as st

from utils.loader import load_cl31, load_cl32
from components.deliverables import build_deliverables_report

st.set_page_config(layout="wide")

st.title("Deliverables Comparison (CL31 vs CL32)")

cl31 = load_cl31()
cl32 = load_cl32()

df = build_deliverables_report(cl31, cl32)

# -----------------------------
# COLOUR RULES
# -----------------------------
def color_status(val):
    if val == "DELAYED":
        return "background-color:#ffcccc"
    if val == "AHEAD":
        return "background-color:#cce5ff"
    if val == "UNCHANGED":
        return "background-color:#e6ffe6"
    if val == "NEW":
        return "background-color:#fff3cd"
    if val == "REMOVED":
        return "background-color:#d6d6d6"
    return ""

styled = (
    df.style
    .map(color_status, subset=["Status"])
    .set_properties(**{
        "font-size": "14px",
        "text-align": "left"
    })
)

st.dataframe(styled, use_container_width=True)