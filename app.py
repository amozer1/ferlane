import streamlit as st
import pandas as pd

from utils.loader import load_excel
from components.deliverables import build_deliverable_comparison


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="CL31 vs CL32 Deliverables Tracker",
    layout="wide"
)

st.title("📊 CL31 vs CL32 Deliverables Comparison Dashboard")


# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df31 = load_excel("data/CL31-February.xlsx")
    df32 = load_excel("data/CL32-May.xlsx")
    return df31, df32


df31, df32 = load_data()


# -----------------------------
# RUN COMPARISON ENGINE
# -----------------------------
comparison_df = build_deliverable_comparison(df31, df32)


# -----------------------------
# FILTERS (Sidebar)
# -----------------------------
st.sidebar.header("Filters")

change_filter = st.sidebar.multiselect(
    "Change Type",
    options=comparison_df["Change Type"].unique(),
    default=comparison_df["Change Type"].unique()
)

search_text = st.sidebar.text_input("Search Deliverable")


filtered_df = comparison_df[
    comparison_df["Change Type"].isin(change_filter)
]

if search_text:
    filtered_df = filtered_df[
        filtered_df["Deliverable"].str.contains(search_text, case=False, na=False)
    ]


# -----------------------------
# SUMMARY CARDS
# -----------------------------
st.subheader("📌 Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(comparison_df))
col2.metric("Delayed", (comparison_df["Change Type"] == "DELAYED").sum())
col3.metric("New", (comparison_df["Change Type"] == "NEW").sum())
col4.metric("Removed", (comparison_df["Change Type"] == "REMOVED").sum())


# -----------------------------
# MAIN TABLE
# -----------------------------
st.subheader("📋 Deliverables Comparison Table")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# DOWNLOAD BUTTON
# -----------------------------
st.download_button(
    label="⬇️ Download Comparison CSV",
    data=filtered_df.to_csv(index=False),
    file_name="cl31_vs_cl32_deliverables.csv",
    mime="text/csv"
)


# -----------------------------
# SIMPLE INSIGHT SECTION
# -----------------------------
st.subheader("📊 Quick Insights")

delayed = comparison_df[comparison_df["Change Type"] == "DELAYED"]
new = comparison_df[comparison_df["Change Type"] == "NEW"]
removed = comparison_df[comparison_df["Change Type"] == "REMOVED"]

st.write(f"🔴 **Most delayed items:** {len(delayed)}")
st.write(f"🟢 **New scope added in CL32:** {len(new)}")
st.write(f"⚫ **Removed from CL32:** {len(removed)}")


# -----------------------------
# OPTIONAL DETAIL EXPANDER
# -----------------------------
with st.expander("🔍 View Raw Comparison Data"):
    st.dataframe(comparison_df, use_container_width=True)