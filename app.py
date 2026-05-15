import streamlit as st
import pandas as pd
from pathlib import Path

from utils.cleaner import clean_programme
from utils.comparison import compare_programmes
from utils.calculations import calculate_deltas
from utils.classifications import classify_activity

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Design Deliverable Tracker",
    layout="wide"
)

st.title("📊 Design Deliverable Tracker Dashboard")
st.markdown("NEC Clause 31 vs Clause 32 Multi-Programme Analysis")

# ======================================================
# DATA SOURCE
# ======================================================

DATA_FOLDER = Path("data")

# ======================================================
# LOAD ALL EXCEL FILES (MULTI-FILE SUPPORT)
# ======================================================

@st.cache_data
def load_all_files():

    files = list(DATA_FOLDER.glob("*.xlsx"))

    if not files:
        st.error("No Excel files found in /data folder")
        st.stop()

    dfs = []

    for f in files:
        df = pd.read_excel(f, engine="openpyxl")
        df["Source File"] = f.name
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


# ======================================================
# SPLIT INTO CL31 / CL32
# ======================================================

def split_programmes(df):

    df31 = df[df["Source File"].str.contains("CL31", na=False)].copy()
    df32 = df[df["Source File"].str.contains("CL32", na=False)].copy()

    return df31, df32


# ======================================================
# PROCESS PIPELINE
# ======================================================

@st.cache_data
def process_data():

    raw = load_all_files()

    df31, df32 = split_programmes(raw)

    if df31.empty or df32.empty:
        st.error("Missing CL31 or CL32 data files")
        st.stop()

    df31 = clean_programme(df31)
    df32 = clean_programme(df32)

    merged = compare_programmes(df31, df32)
    merged = calculate_deltas(merged)

    merged["Status"] = merged.apply(classify_activity, axis=1)

    return merged


merged = process_data()

# ======================================================
# KPI SECTION (EXECUTIVE VIEW)
# ======================================================

total = len(merged)
delayed = len(merged[merged["Status"] == "Delayed"])
accelerated = len(merged[merged["Status"] == "Accelerated"])
on_track = len(merged[merged["Status"] == "On Track"])

delay_pct = (delayed / total) * 100 if total else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Total Activities", total)

with kpi2:
    st.metric("Delayed", delayed)

with kpi3:
    st.metric("Accelerated", accelerated)

with kpi4:
    st.metric("On Track", on_track)

st.markdown("---")

# ======================================================
# FILE VISIBILITY PANEL (NEW - IMPORTANT FOR MULTI FILES)
# ======================================================

st.subheader("📁 Programme Sources")

file_summary = merged.groupby("Source File").size().reset_index(name="Activities")

st.dataframe(file_summary, use_container_width=True)

st.markdown("---")

# ======================================================
# VISUAL ANALYTICS
# ======================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Status Breakdown")

    chart_df = pd.DataFrame({
        "Status": ["Delayed", "Accelerated", "On Track"],
        "Count": [delayed, accelerated, on_track]
    })

    st.bar_chart(chart_df.set_index("Status"))

with col2:
    st.subheader("📈 Project Health")

    st.progress(int(100 - delay_pct))

    st.markdown(
        f"""
        **Delay Exposure:** {delay_pct:.1f}%  

        **Health Status:**
        {'🔴 Critical' if delay_pct > 20 else '🟡 Moderate' if delay_pct > 10 else '🟢 Healthy'}
        """
    )

st.markdown("---")

# ======================================================
# FILTER PANEL
# ======================================================

st.subheader("🔍 Filters & Search")

c1, c2, c3 = st.columns([2, 2, 3])

with c1:
    status_filter = st.selectbox(
        "Status",
        ["All", "Delayed", "Accelerated", "On Track", "New Activity", "Removed"]
    )

with c2:
    file_filter = st.selectbox(
        "Source File",
        ["All"] + sorted(merged["Source File"].unique().tolist())
    )

with c3:
    search = st.text_input("Search Activity ID / Name")

filtered = merged.copy()

if status_filter != "All":
    filtered = filtered[filtered["Status"] == status_filter]

if file_filter != "All":
    filtered = filtered[filtered["Source File"] == file_filter]

if search:
    filtered = filtered[
        filtered["Activity ID"].astype(str).str.contains(search, case=False, na=False) |
        filtered["Activity Name_31"].astype(str).str.contains(search, case=False, na=False)
    ]

# ======================================================
# TABLE VIEW (DETAIL LAYER)
# ======================================================

st.subheader("📋 Programme Comparison Table")

st.dataframe(
    filtered[
        [
            "Source File",
            "Activity ID",
            "Activity Name_31",
            "Start_31",
            "Finish_31",
            "Start_32",
            "Finish_32",
            "Delta Start Days",
            "Delta Finish Days",
            "Float Variance",
            "Status"
        ]
    ],
    use_container_width=True,
    height=600
)

# ======================================================
# EXPORT
# ======================================================

st.download_button(
    "📥 Export Filtered Programme",
    data=filtered.to_csv(index=False),
    file_name="design_deliverable_tracker_multi.csv",
    mime="text/csv"
)