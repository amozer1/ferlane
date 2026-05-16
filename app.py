import streamlit as st

from utils import loader
from components.deliverables import compare_deliverables

st.set_page_config(page_title="Deliverable Tracker", layout="wide")

st.title("📊 Deliverable Comparison (CL31 vs CL32)")


# =========================
# LOAD DATA
# =========================
df31 = loader.load_cl31()
df32 = loader.load_cl32()


# =========================
# PROCESS
# =========================
df = compare_deliverables(df31, df32)


# =========================
# FILTERS
# =========================
st.sidebar.header("Filters")

change_filter = st.sidebar.multiselect(
    "Change Type",
    ["DELAYED", "AHEAD", "UNCHANGED", "NEW", "REMOVED"],
    default=["DELAYED", "NEW", "REMOVED", "AHEAD"]
)

filtered = df[df["Change Type"].isin(change_filter)]


# =========================
# SUMMARY
# =========================
st.subheader("Summary")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Deliverables", len(df))
c2.metric("Delayed", (df["Change Type"] == "DELAYED").sum())
c3.metric("Ahead", (df["Change Type"] == "AHEAD").sum())
c4.metric("New", (df["Change Type"] == "NEW").sum())
c5.metric("Removed", (df["Change Type"] == "REMOVED").sum())


# =========================
# TABLE
# =========================
st.subheader("Deliverable Comparison Table")

st.dataframe(
    filtered.sort_values("Delta (Days)", ascending=False),
    use_container_width=True
)


# =========================
# DOWNLOAD
# =========================
st.download_button(
    "Download Report",
    data=filtered.to_csv(index=False),
    file_name="Deliverable_Comparison.csv",
    mime="text/csv"
)