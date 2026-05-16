import streamlit as st
from utils.loader import load_cl31, load_cl32
from components.deliverables import build_comparison

st.set_page_config(page_title="Programme Delta Tracker", layout="wide")

st.title("CL31 vs CL32 Programme Comparison")

# Load data
df31 = load_cl31()
df32 = load_cl32()

# Build comparison
df = build_comparison(df31, df32)

# =========================
# FILTERS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    change_filter = st.multiselect(
        "Change Type",
        ["DELAYED", "AHEAD", "UNCHANGED", "NEW", "REMOVED"],
        default=["DELAYED", "AHEAD", "NEW", "REMOVED"]
    )

filtered_df = df[df["Change Type"].isin(change_filter)]

# =========================
# METRICS
# =========================
st.subheader("Summary")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Items", len(df))
c2.metric("Delayed", (df["Change Type"] == "DELAYED").sum())
c3.metric("Ahead", (df["Change Type"] == "AHEAD").sum())
c4.metric("New", (df["Change Type"] == "NEW").sum())
c5.metric("Removed", (df["Change Type"] == "REMOVED").sum())

# =========================
# MAIN TABLE
# =========================
st.subheader("Delta Comparison Table")

st.dataframe(
    filtered_df.sort_values(by="Delta (Days)", ascending=False),
    use_container_width=True
)

# =========================
# DOWNLOAD
# =========================
st.download_button(
    "Download Comparison",
    data=filtered_df.to_csv(index=False),
    file_name="CL31_vs_CL32_Delta.csv",
    mime="text/csv"
)