# app.py
import streamlit as st
from loader import load_programmes
from deliverables import compare

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="CL Deliverables Tracker", layout="wide")

st.title("📊 CL31-Feb vs CL32-May Deliverables Tracker")


# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def get_data():
    cl31, cl32 = load_programmes()
    return compare(cl31, cl32)


df = get_data()


# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(df))
col2.metric("Delayed", len(df[df["change_type"] == "DELAYED"]))
col3.metric("New", len(df[df["change_type"] == "NEW"]))
col4.metric("Removed", len(df[df["change_type"] == "REMOVED"]))


# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

types = df["change_type"].dropna().unique()

selected = st.sidebar.multiselect(
    "Change Type Filter",
    types,
    default=types
)

filtered = df[df["change_type"].isin(selected)]


# -----------------------------
# TABLE OUTPUT
# -----------------------------
st.subheader("Deliverable Comparison Table")

st.dataframe(
    filtered[[
        "deliverable",
        "cl31_finish",
        "cl32_finish",
        "delta_days",
        "change_type",
        "status_comment"
    ]],
    use_container_width=True
)


# -----------------------------
# DOWNLOAD
# -----------------------------
csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download CSV",
    csv,
    "deliverables_cl31_cl32_comparison.csv",
    "text/csv"
)