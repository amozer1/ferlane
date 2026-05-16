import pandas as pd
import numpy as np
import re

DATE_FORMAT = "%d-%b-%Y"


# -----------------------------
# CLEAN DATE FUNCTION
# -----------------------------
def clean_date(val):
    if pd.isna(val):
        return np.nan

    val = str(val).strip()

    # remove A, *, etc.
    val = re.sub(r"[A\*]", "", val).strip()

    # try parse datetime
    try:
        dt = pd.to_datetime(val, errors="coerce")
        if pd.isna(dt):
            return np.nan
        return dt
    except:
        return np.nan


# -----------------------------
# LOAD PROGRAMME FILE
# -----------------------------
def load_programme(file):
    if file is None:
        return pd.DataFrame()

    df = pd.read_excel(file, engine="openpyxl")

    # standardise column names
    df.columns = [c.strip() for c in df.columns]

    # detect activity name column
    name_col = None
    for c in df.columns:
        if "activity" in c.lower() or "deliverable" in c.lower():
            name_col = c
            break

    if name_col is None:
        raise ValueError("No Activity Name column found")

    finish_col = None
    for c in df.columns:
        if "finish" in c.lower():
            finish_col = c
            break

    df = df[[name_col, finish_col]].copy()
    df.columns = ["Deliverable", "Finish"]

    # clean
    df["Deliverable"] = df["Deliverable"].astype(str).str.strip()
    df["Finish"] = df["Finish"].apply(clean_date)

    # remove invalid rows (IMPORTANT FIX YOU REQUESTED)
    df = df.dropna(subset=["Deliverable"])
    df = df.dropna(subset=["Finish"])

    return df


# -----------------------------
# FORMAT DATE
# -----------------------------
def fmt_date(x):
    if pd.isna(x):
        return "—"
    return pd.to_datetime(x).strftime(DATE_FORMAT)


# -----------------------------
# COMPARISON ENGINE
# -----------------------------
def prepare_comparison_df(file31, file32):
    df31 = load_programme(file31)
    df32 = load_programme(file32)

    # merge on Deliverable
    merged = pd.merge(
        df31,
        df32,
        on="Deliverable",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # clean rename
    merged = merged.rename(columns={
        "Finish_CL31": "CL31 Finish",
        "Finish_CL32": "CL32 Finish"
    })

    # change classification
    def classify(row):
        a = row["CL31 Finish"]
        b = row["CL32 Finish"]

        if pd.notna(a) and pd.notna(b):
            if a == b:
                return "UNCHANGED"
            return "MODIFIED"

        if pd.isna(a) and pd.notna(b):
            return "NEW"

        if pd.notna(a) and pd.isna(b):
            return "REMOVED"

        return "UNKNOWN"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # delta calc
    def delta(row):
        a = row["CL31 Finish"]
        b = row["CL32 Finish"]

        if pd.isna(a) or pd.isna(b):
            return None

        return (pd.to_datetime(b) - pd.to_datetime(a)).days

    merged["Delta (Days)"] = merged.apply(delta, axis=1)

    # status comments
    def comment(row):
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "MODIFIED":
            return "Date adjusted vs baseline"
        if row["Change Type"] == "NEW":
            return "Added in CL32"
        if row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        return "Stable"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    # format dates for dashboard
    merged["CL31 Finish"] = merged["CL31 Finish"].apply(fmt_date)
    merged["CL32 Finish"] = merged["CL32 Finish"].apply(fmt_date)

    # reorder
    merged = merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return merged