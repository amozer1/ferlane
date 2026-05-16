import pandas as pd
import numpy as np


# -----------------------------
# 1. Identify TRUE deliverables
# -----------------------------
def is_deliverable(text: str) -> bool:
    if pd.isna(text):
        return False

    text = str(text).lower()

    # 🚫 filter noise (THIS FIXES your "site visit is deliverable" issue)
    exclude_keywords = [
        "site", "visit", "mobilisation", "mobilization",
        "governance", "meeting", "review", "submit",
        "approval", "issue", "install", "temporary",
        "procurement", "design pack", "kick off"
    ]

    # keep only high-level outputs
    include_keywords = [
        "design", "shaft", "outline", "package", "tank",
        "rising main", "storm", "eica", "mechanical",
        "civil", "instrumentation", "control", "concept",
        "freeze"
    ]

    if any(k in text for k in exclude_keywords):
        return False

    if any(k in text for k in include_keywords):
        return True

    return False


# -----------------------------
# 2. Normalize date format
# -----------------------------
def clean_date(x):
    if pd.isna(x) or x == "" or str(x).strip() == "—":
        return None

    try:
        return pd.to_datetime(x).strftime("%d-%b-%y")
    except:
        return None


# -----------------------------
# 3. Build deliverable table
# -----------------------------
def build_deliverable_delta(df31: pd.DataFrame, df32: pd.DataFrame):
    # EXPECTED columns (safe fallback)
    df31 = df31.copy()
    df32 = df32.copy()

    # normalize column names
    df31.columns = df31.columns.str.strip()
    df32.columns = df32.columns.str.strip()

    # try to detect columns safely
    name_col = "Activity Name"
    date_col = "Finish"

    # FILTER deliverables only
    d31 = df31[df31[name_col].apply(is_deliverable)][[name_col, date_col]]
    d32 = df32[df32[name_col].apply(is_deliverable)][[name_col, date_col]]

    d31 = d31.rename(columns={date_col: "CL31 Finish"})
    d32 = d32.rename(columns={date_col: "CL32 Finish"})

    # merge
    merged = pd.merge(
        d31,
        d32,
        on=name_col,
        how="outer"
    )

    merged.columns = ["Deliverable", "CL31 Finish", "CL32 Finish"]

    # clean dates
    merged["CL31 Finish"] = merged["CL31 Finish"].apply(clean_date)
    merged["CL32 Finish"] = merged["CL32 Finish"].apply(clean_date)

    # -----------------------------
    # 4. DELTA LOGIC
    # -----------------------------
    def calc_delta(row):
        try:
            if row["CL31 Finish"] and row["CL32 Finish"]:
                d31 = pd.to_datetime(row["CL31 Finish"])
                d32 = pd.to_datetime(row["CL32 Finish"])
                return (d32 - d31).days
        except:
            return None
        return None

    merged["Delta (Days)"] = merged.apply(calc_delta, axis=1)

    # -----------------------------
    # 5. CHANGE TYPE LOGIC
    # -----------------------------
    def change_type(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        if row["Delta (Days)"] == 0:
            return "UNCHANGED"
        if row["Delta (Days)"] and row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] and row["Delta (Days)"] < 0:
            return "ADVANCED"
        return "UNKNOWN"

    merged["Change Type"] = merged.apply(change_type, axis=1)

    # -----------------------------
    # 6. COMMENT LOGIC
    # -----------------------------
    def comment(row):
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "ADVANCED":
            return "Pulled forward, programme gain"
        if row["Change Type"] == "NEW":
            return "Added scope in CL32"
        if row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        return "Stable"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    # final column order
    merged = merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return merged