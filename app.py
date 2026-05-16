import streamlit as st
from loader import load_schedule, standardise_dates
from deliverables import build_comparison

st.set_page_config(page_title="CL31 vs CL32 Deliverables", layout="wide")

st.title("CL31 vs CL32 Deliverable Comparison")

# ------------------------
# Load data automatically
# ------------------------
cl31_path = "data/CL31.xlsx"
cl32_path = "data/CL32.xlsx"

df31 = standardise_dates(load_schedule(cl31_path))
df32 = standardise_dates(load_schedule(cl32_path))

# ------------------------
# Build comparison
# ------------------------
result = build_comparison(df31, df32)

# ------------------------
# Clean display (NO FILTERS)
# ------------------------
def colour_row(row):
    if row["Change Type"] == "DELAYED":
        return ["background-color: #ffcccc"] * len(row)
    elif row["Change Type"] == "ACCELERATED":
        return ["background-color: #ccffcc"] * len(row)
    elif row["Change Type"] == "NEW":
        return ["background-color: #cce5ff"] * len(row)
    elif row["Change Type"] == "REMOVED":
        return ["background-color: #ffe5cc"] * len(row)
    return [""] * len(row)

st.dataframe(
    result.style.apply(colour_row, axis=1),
    use_container_width=True
)