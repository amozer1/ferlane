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

st.markdown("---")

# ======================================================
# DATA FOLDER
# ======================================================

DATA_FOLDER = Path("data")

# ======================================================
# SAFE DATA LOADER (FIXES YOUR ERROR)
# ======================================================

@st.cache_data
def load_all_files():

    files = list(DATA_FOLDER.glob("*.xlsx"))

    if len(files) == 0:
        st.error("No .xlsx files found in /data folder")
        st.stop()

    df_list = []

    for file in files:

        df = pd.read_excel(file, engine="openpyxl")

        # 🔥 FORCE SAFE COLUMN CREATION
        df = df.copy()
        df["Source File"] = file.name

        df_list.append(df)

    combined = pd.concat(df_list, ignore_index=True)

    # 🔥 HARD SAFETY CHECK
    if "Source File" not in combined.columns:
        st.error("Critical Error: 'Source File' column missing after load")
        st.stop()

    return combined


# ======================================================
# SPLIT CL31 / CL32 SAFELY
# ======================================================

def split_programmes(df):

    if "Source File" not in df.columns:
        st.error("Missing 'Source File' column. Reload data.")
        st.stop()

    df31 = df[df["Source File"].astype(str).str.contains("CL31", na=False)].copy()
    df32 = df[df["Source File"].astype(str).str.contains("CL32", na=False)].copy()

    return df31, df32


# ======================================================
# BUILD PIPELINE (FULL PROCESS)
# ======================================================

@st.cache_data
def build_data():

    raw = load_all_files()

    df31, df32 = split_programmes(raw)

    if df31.empty:
        st.error("No CL31 data found in files")
        st.stop()

    if df32.empty:
        st.error("No CL32 data found in files")
        st.stop()

    # PROCESSING PIPELINE
    df31 = clean_programme(df31)
    df32 = clean_programme(df32)

    merged = compare_programmes(df31, df32)
    merged = calculate_deltas(merged)

    merged["Status"] = merged.apply(classify_activity, axis=1)

    return merged


df = build_data()

# ======================================================
# SIDEBAR FILTERS
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

search = st.sidebar.text_input("Search Activity ID / Name")

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
# KPI SECTION
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
# VISUAL SECTION
# ======================================================

st.markdown("## 📊 Programme Overview")

col1, col2 = st.columns(2)

with col1:

    chart_df = pd.DataFrame({
        "Status": ["Delayed", "Accelerated", "On Track"],
        "Count": [delayed, accelerated, on_track]
    })

    st.bar_chart(chart_df.set_index("Status"))

with col2:

    st.metric("Delay Exposure (%)", f"{delay_pct:.1f}%")

    st.progress(int(max(0, min(100, 100 - delay_pct))))

    if delay_pct > 20:
        st.error("🔴 Critical Programme Risk")
    elif delay_pct > 10:
        st.warning("🟡 Moderate Risk")
    else:
        st.success("🟢 Healthy Programme")

st.markdown("---")

# ======================================================
# DATA TABLE
# ======================================================

st.markdown("## 📋 Programme Register")

required_cols = [
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

# SAFE COLUMN CHECK
existing_cols = [c for c in required_cols if c in filtered.columns]

st.dataframe(
    filtered[existing_cols],
    use_container_width=True,
    height=600
)

# ======================================================
# EXPORT
# ======================================================

st.download_button(
    "📥 Export Data",
    data=filtered.to_csv(index=False),
    file_name="design_deliverable_tracker.csv",
    mime="text/csv"
)