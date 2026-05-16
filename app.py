import streamlit as st
from utils.loader import load_cl31, load_cl32
from components.deliverables import build_design_control_table

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(layout="wide")
st.title("Design Management Control Dashboard (CL31 vs CL32)")

# -------------------------
# LOAD DATA
# -------------------------
cl31 = load_cl31("data/CL31.xlsx")
cl32 = load_cl32("data/CL32.xlsx")

# -------------------------
# BUILD CONTROL TABLE
# -------------------------
df = build_design_control_table(cl31, cl32)

# -------------------------
# SAFETY CHECK (CRITICAL FIX)
# prevents KeyError like 'Discipline'
# -------------------------
if "Status" not in df.columns:
    df["Status"] = "🟡 No Update"

if "Discipline" not in df.columns:
    df["Discipline"] = "Unknown"

# -------------------------
# FILTER OPTIONS (SAFE)
# -------------------------
status_options = sorted(df["Status"].dropna().unique())
discipline_options = sorted(df["Discipline"].dropna().unique())

# -------------------------
# FILTER UI
# -------------------------
col1, col2 = st.columns(2)

with col1:
    status_filter = st.multiselect(
        "Filter Status",
        options=status_options,
        default=status_options
    )

with col2:
    discipline_filter = st.multiselect(
        "Filter Discipline",
        options=discipline_options,
        default=discipline_options
    )

# -------------------------
# APPLY FILTERS
# -------------------------
filtered_df = df[
    df["Status"].isin(status_filter) &
    df["Discipline"].isin(discipline_filter)
]

# -------------------------
# COLOUR STYLING
# -------------------------
def style(row):
    status = str(row.get("Status", ""))

    if "🔴" in status:
        return ["background-color:#ffcccc"] * len(row)
    if "🟠" in status:
        return ["background-color:#ffe5cc"] * len(row)
    if "🟡" in status:
        return ["background-color:#fff7cc"] * len(row)
    if "🟢" in status:
        return ["background-color:#e6ffe6"] * len(row)

    return [""] * len(row)

# -------------------------
# DISPLAY TABLE
# -------------------------
st.dataframe(
    filtered_df.style.apply(style, axis=1),
    use_container_width=True,
    height=700
)

# -------------------------
# QUICK SUMMARY (MEETING VALUE)
# -------------------------
st.markdown("### 📊 Summary")

colA, colB, colC, colD = st.columns(4)

colA.metric("Total Activities", len(df))
colB.metric("🔴 Critical", (df["Status"] == "🔴 Critical Delay").sum())
colC.metric("🟠 At Risk", (df["Status"] == "🟠 At Risk").sum())
colD.metric("🟢 Ahead", (df["Status"] == "🟢 Ahead").sum())