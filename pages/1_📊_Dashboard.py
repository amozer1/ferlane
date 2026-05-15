import streamlit as st
import pandas as pd
from pathlib import Path

from utils.cleaner import clean_programme
from utils.comparison import compare_programmes
from utils.calculations import calculate_deltas
from utils.classifications import classify_activity

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

# ======================================================
# HEADER
# ======================================================

st.title("📊 Design Deliverable Tracker")
st.markdown("### NEC Clause 31 vs Clause 32 Programme Dashboard")

st.markdown("---")

# ======================================================
# DATA LOADING LAYER (MULTI FILE READY)
# ======================================================

DATA_FOLDER = Path("data")

@st.cache_data
def load_raw_data():

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


def split_programmes(df):

    df31 = df[df["Source File"].str.contains("CL31", na=False)].copy()
    df32 = df[df["Source File"].str.contains("CL32", na=False)].copy()

    return df31, df32


@st.cache_data
def build_dashboard_data():

    raw = load_raw_data()

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


df = build_dashboard_data()

# ======================================================
# FILTERS (CONTROL PANEL STYLE)
# ======================================================

st.sidebar.header("🎛 Filters")

status_filter = st.sidebar.selectbox(
    "Status",
    ["All", "Delayed", "Accelerated", "On Track", "New Activity", "Removed"]
)

file_filter = st.sidebar.selectbox(
    "Source File",
    ["All"] + sorted(df["Source File"].unique().tolist())
)

search = st.sidebar.text_input("Search Activity")

filtered = df.copy()

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
# KPI SECTION (EXECUTIVE VIEW)
# ======================================================

total = len(filtered)
delayed = len(filtered[filtered["Status"] == "Delayed"])
accelerated = len(filtered[filtered["Status"] == "Accelerated"])
on_track = len(filtered[filtered["Status"] == "On Track"])

delay_pct = (delayed / total) * 100 if total else 0

st.markdown("## 📌 Executive Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Activities", total)
c2.metric("Delayed", delayed)
c3.metric("Accelerated", accelerated)
c4.metric("On Track", on_track)

st.markdown("---")

# ======================================================
# VISUAL SECTION (PROPER DASHBOARD BLOCK)
# ======================================================

st.markdown("## 📊 Programme Performance Overview")

left, right = st.columns(2)

with left:

    chart_data = pd.DataFrame({
        "Status": ["Delayed", "Accelerated", "On Track"],
        "Count": [delayed, accelerated, on_track]
    })

    st.bar_chart(chart_data.set_index("Status"))

with right:

    st.metric("Delay Exposure (%)", f"{delay_pct:.1f}%")

    st.progress(int(max(0, min(100, 100 - delay_pct))))

    st.markdown(
        f"""
        ### Project Health

        {"🔴 Critical" if delay_pct > 20 else "🟡 Moderate" if delay_pct > 10 else "🟢 Healthy"}
        """
    )

st.markdown("---")

# ======================================================
# DATA TABLE (CORE CONTROL VIEW)
# ======================================================

st.markdown("## 📋 Activity Register")

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
# EXPORT SECTION
# ======================================================

st.markdown("---")

st.download_button(
    "📥 Export Filtered Programme",
    data=filtered.to_csv(index=False),
    file_name="programme_dashboard_export.csv",
    mime="text/csv"
)