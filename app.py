import streamlit as st
from utils.loader import load_cl31, load_cl32
from components.deliverables import build_deliverable_delta

st.set_page_config(layout="wide")

st.title("CL31 vs CL32 Deliverable Delta Tracker")

df31 = load_cl31()
df32 = load_cl32()

result = build_deliverable_delta(df31, df32)

# -----------------------------
# COLOUR LOGIC (NO applymap error)
# -----------------------------
def color_rows(row):
    if row["Change Type"] == "DELAYED":
        return ["background-color: #ffcccc"] * len(row)
    if row["Change Type"] == "ADVANCED":
        return ["background-color: #cce5ff"] * len(row)
    if row["Change Type"] == "NEW":
        return ["background-color: #d4edda"] * len(row)
    if row["Change Type"] == "REMOVED":
        return ["background-color: #f8d7da"] * len(row)
    return [""] * len(row)

styled = result.style.apply(color_rows, axis=1)

st.dataframe(styled, use_container_width=True)