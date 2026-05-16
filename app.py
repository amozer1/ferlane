import streamlit as st

from utils.loader import load_cl31, load_cl32
from components.deliverables import build_deliverables_report

st.set_page_config(layout="wide")

st.title("Deliverables Comparison (CL31 vs CL32)")

cl31 = load_cl31()
cl32 = load_cl32()

df = build_deliverables_report(cl31, cl32)

# -----------------------------
# COLOUR LOGIC
# -----------------------------
def color_status(val):
    if val == "DELAYED":
        return "background-color: #ffcccc; color: black;"
    if val == "AHEAD":
        return "background-color: #cce5ff; color: black;"
    if val == "UNCHANGED":
        return "background-color: #e6ffe6; color: black;"
    if val == "NEW":
        return "background-color: #fff3cd; color: black;"
    if val == "REMOVED":
        return "background-color: #d6d6d6; color: black;"
    return ""

def color_delta(val):
    if pd.isna(val):
        return ""
    if val > 0:
        return "color: red; font-weight: bold;"
    if val < 0:
        return "color: green; font-weight: bold;"
    return "color: black;"

styled_df = (
    df.style
    .applymap(color_status, subset=["Status"])
    .applymap(color_delta, subset=["Delta (Days)"])
    .set_properties(**{
        "text-align": "left",
        "font-size": "14px"
    })
)

st.dataframe(styled_df, use_container_width=True)