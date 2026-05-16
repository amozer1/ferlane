# app.py
import pandas as pd
import streamlit as st
import re

# =========================
# 1. CONFIG
# =========================

st.set_page_config(page_title="CL31 vs CL32 Comparator", layout="wide")

# =========================
# 2. LOAD DATA
# =========================

@st.cache_data
def load_data(cl31_path, cl32_path):
    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)
    return cl31, cl32


# =========================
# 3. DELIVERABLE EXTRACTION LOGIC
# =========================

REMOVE_WORDS = [
    "review", "raise", "rfis", "tq", "meeting", "workshop",
    "develop", "check", "update", "model", "modelling",
    "analysis", "prepare", "formulate", "generate"
]

KEEP_HINTS = [
    "design", "drawing", "submission", "pack", "report",
    "assessment", "calculation", "calcs", "plan", "schedule",
    "specification", "commissioning", "handover", "completion",
    "freeze", "concept", "detail", "ga"
]


def extract_deliverable(text):
    if pd.isna(text):
        return None

    text = str(text).lower()

    # Remove brackets content like [GET]
    text = re.sub(r"\[.*?\]", "", text)

    # Remove extra symbols
    text = re.sub(r"[^a-z0-9 ]", " ", text)

    words = text.split()

    # If contains strong deliverable keyword → keep core phrase
    if any(k in text for k in KEEP_HINTS):
        cleaned = " ".join([w for w in words if w not in REMOVE_WORDS])
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned.title()

    return None


# =========================
# 4. PREPROCESS SCHEDULE
# =========================

def preprocess(df, finish_col, label):
    df = df.copy()

    # Detect activity name column (robust)
    name_col = [c for c in df.columns if "name" in c.lower()]
    if not name_col:
        raise ValueError(f"No Activity Name column in {label}")
    name_col = name_col[0]

    df["Deliverable"] = df[name_col].apply(extract_deliverable)
    df = df.dropna(subset=["Deliverable"])

    df = df[[ "Deliverable", finish_col ]].rename(columns={finish_col: f"{label}_Finish"})

    return df


# =========================
# 5. MATCHING ENGINE
# =========================

def build_comparison(cl31, cl32):

    merged = pd.merge(
        cl31,
        cl32,
        on="Deliverable",
        how="outer"
    )

    # Ensure datetime
    for col in merged.columns:
        if "Finish" in col:
            merged[col] = pd.to_datetime(merged[col], errors="coerce")

    # Delta calculation
    merged["Delta (Days)"] = (
        merged["CL32_Finish"] - merged["CL31_Finish"]
    ).dt.days

    # Change Type
    def classify(row):
        if pd.isna(row["CL31_Finish"]) and not pd.isna(row["CL32_Finish"]):
            return "NEW"
        if pd.isna(row["CL32_Finish"]) and not pd.isna(row["CL31_Finish"]):
            return "REMOVED"
        if pd.isna(row["Delta (Days)"]):
            return "UNKNOWN"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] < 0:
            return "AHEAD"
        return "UNCHANGED"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # Status / comment
    def comment(row):
        if row["Change Type"] == "NEW":
            return "Added in CL32 scope"
        if row["Change Type"] == "REMOVED":
            return "Removed from CL32"
        if row["Change Type"] == "DELAYED":
            return "Shifted later in programme"
        if row["Change Type"] == "AHEAD":
            return "Pulled forward"
        return "No change"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    return merged


# =========================
# 6. STREAMLIT UI
# =========================

st.title("📊 CL31 vs CL32 Deliverable Comparison Engine")

cl31_file = st.file_uploader("Upload CL31 file", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32 file", type=["xlsx"])

if cl31_file and cl32_file:

    cl31_raw, cl32_raw = load_data(cl31_file, cl32_file)

    # Adjust finish column names if needed
    cl31_processed = preprocess(cl31_raw, "BL Project Finish", "CL31")
    cl32_processed = preprocess(cl32_raw, "BL1 Finish", "CL32")

    result = build_comparison(cl31_processed, cl32_processed)

    # Format output
    result = result[[
        "Deliverable",
        "CL31_Finish",
        "CL32_Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    # Sort logic
    result = result.sort_values(by=["Change Type", "Delta (Days)"], ascending=[False, False])

    st.subheader("📌 Deliverable Comparison Table")

    st.dataframe(
        result.style.apply(
            lambda x: [
                "background-color: #ffcccc" if v == "DELAYED"
                else "background-color: #ccffcc" if v == "AHEAD"
                else "background-color: #ffffcc" if v == "NEW"
                else "background-color: #eeeeee"
                for v in x["Change Type"]
            ],
            axis=1
        ),
        use_container_width=True
    )

    # Summary
    st.subheader("📊 Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Deliverables", len(result))
    col2.metric("Delayed", (result["Change Type"] == "DELAYED").sum())
    col3.metric("Ahead", (result["Change Type"] == "AHEAD").sum())
    col4.metric("New Items", (result["Change Type"] == "NEW").sum())

else:
    st.info("Upload both CL31 and CL32 Excel files to generate comparison")