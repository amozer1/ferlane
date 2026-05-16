import streamlit as st
from utils.loader import load_cl31, load_cl32
from components.deliverables import build_design_control_table

st.set_page_config(layout="wide")

st.title("Design Management Control Dashboard (CL31 vs CL32)")

# -------------------------
# LOAD DATA
# -------------------------
cl31 = load_cl31("data/CL31.xlsx")
cl32 = load_cl32("data/CL32.xlsx")

# -------------------------
# BUILD TABLE
# -------------------------
df = build_design_control_table(cl31, cl32)

# -------------------------
# SAFE FILTERS
# -------------------------
col1, col2 = st.columns(2)

with col1:
    status_filter = st.multiselect(
        "Filter Status",
        options=df["Status"].dropna().unique(),
        default=df["Status"].dropna().unique()
    )

with col2:
    discipline_filter = st.multiselect(
        "Filter Discipline",
        options=df["Discipline"].dropna().unique(),
        default=df["Discipline"].dropna().unique()
    )

filtered_df = df[
    df["Status"].isin(status_filter) &
    df["Discipline"].isin(discipline_filter)
]

# -------------------------
# STYLING
# -------------------------
def style(row):
    if "🔴" in str(row["Status"]):
        return ["background-color:#ffcccc"] * len(row)
    if "🟠" in str(row["Status"]):
        return ["background-color:#ffe5cc"] * len(row)
    if "🟡" in str(row["Status"]):
        return ["background-color:#fff7cc"] * len(row)
    if "🟢" in str(row["Status"]):
        return ["background-color:#e6ffe6"] * len(row)
    return [""] * len(row)

st.dataframe(
    filtered_df.style.apply(style, axis=1),
    use_container_width=True
)