import streamlit as st
from loader import load_cl31, load_cl32
from deliverables import build_deliverables

st.set_page_config(layout="wide")

st.title("📊 CL31 vs CL32 Tracker")

df31 = load_cl31()
df32 = load_cl32()

result = build_deliverables(df31, df32)

# =========================
# COLOUR CODING
# =========================
def colour(row):
    if row["Change Type"] == "DELAYED":
        return ["background-color: #ffcccc"] * len(row)
    if row["Change Type"] == "EARLY":
        return ["background-color: #d4edda"] * len(row)
    if row["Change Type"] == "NEW":
        return ["background-color: #cce5ff"] * len(row)
    if row["Change Type"] == "REMOVED":
        return ["background-color: #f8d7da"] * len(row)
    return [""] * len(row)


st.subheader("Deliverable Comparison Table")

styled = result.style.apply(colour, axis=1)

st.dataframe(styled, use_container_width=True)