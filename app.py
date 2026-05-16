import streamlit as st
from loader import load_programme
from deliverables import extract_deliverables, compare_cl31_cl32

st.set_page_config(page_title="Programme Deliverables Tracker", layout="wide")

st.title("📊 CL31 vs CL32 Deliverables Comparison")

# AUTO LOAD FILES (no manual clicks required)
CL31_FILE = "data/CL31.xlsx"
CL32_FILE = "data/CL32.xlsx"

df31_raw = load_programme(CL31_FILE)
df32_raw = load_programme(CL32_FILE)

# Extract deliverables dynamically
df31 = extract_deliverables(df31_raw)
df32 = extract_deliverables(df32_raw)

# Compare
result = compare_cl31_cl32(df31, df32)

# Status logic (visual layer)
def status(row):
    if row["Change Type"] == "DELAYED":
        return "🔴 Delayed"
    if row["Change Type"] == "AHEAD":
        return "🟢 Ahead"
    if row["Change Type"] == "NEW":
        return "🟡 New"
    if row["Change Type"] == "REMOVED":
        return "⚫ Removed"
    return "⚪ Unchanged"

result["Status / Comment"] = result.apply(status, axis=1)

# Display
st.dataframe(result, use_container_width=True)

# Summary
st.subheader("Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(result))
col2.metric("Delayed", (result["Change Type"] == "DELAYED").sum())
col3.metric("New", (result["Change Type"] == "NEW").sum())
col4.metric("Removed", (result["Change Type"] == "REMOVED").sum())