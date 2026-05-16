import pandas as pd
import numpy as np
import re

DATE_FORMAT = "%d-%b-%Y"


# ---------------------------------
# CLEAN DATE
# ---------------------------------
def clean_date(value):

    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # remove A and *
    value = re.sub(r"[A\*]", "", value).strip()

    try:
        dt = pd.to_datetime(value, dayfirst=True, errors="coerce")

        if pd.isna(dt):
            return np.nan

        return dt

    except:
        return np.nan


# ---------------------------------
# FORMAT DATE
# ---------------------------------
def format_date(dt):

    if pd.isna(dt):
        return "—"

    return dt.strftime(DATE_FORMAT)


# ---------------------------------
# LOAD PROGRAMME
# ---------------------------------
def load_programme(file):

    df = pd.read_excel(file, engine="openpyxl")

    df.columns = [c.strip() for c in df.columns]

    # detect activity name column
    activity_col = None

    for c in df.columns:

        c_lower = c.lower()

        if "activity name" in c_lower:
            activity_col = c
            break

    # detect finish column
    finish_col = None

    for c in df.columns:

        c_lower = c.lower()

        if "finish" == c_lower or "finish date" in c_lower:
            finish_col = c
            break

    if activity_col is None:
        raise ValueError("Activity Name column not found")

    if finish_col is None:
        raise ValueError("Finish column not found")

    # keep only required columns
    df = df[[activity_col, finish_col]].copy()

    df.columns = ["Deliverable", "Finish"]

    # clean
    df["Deliverable"] = df["Deliverable"].astype(str).str.strip()

    df["Finish"] = df["Finish"].apply(clean_date)

    # REMOVE BLANK DATES
    df = df.dropna(subset=["Finish"])

    # REMOVE BLANK NAMES
    df = df[df["Deliverable"] != ""]

    # remove duplicates
    df = df.drop_duplicates(subset=["Deliverable"])

    return df


# ---------------------------------
# PREPARE COMPARISON
# ---------------------------------
def prepare_comparison_df(file31, file32):

    df31 = load_programme(file31)
    df32 = load_programme(file32)

    merged = pd.merge(
        df31,
        df32,
        on="Deliverable",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    merged.rename(columns={
        "Finish_CL31": "CL31 Finish",
        "Finish_CL32": "CL32 Finish"
    }, inplace=True)

    # ---------------------------------
    # DELTA
    # ---------------------------------
    def calculate_delta(row):

        a = row["CL31 Finish"]
        b = row["CL32 Finish"]

        if pd.isna(a) or pd.isna(b):
            return "—"

        return int((b - a).days)

    merged["Delta (Days)"] = merged.apply(calculate_delta, axis=1)

    # ---------------------------------
    # CHANGE TYPE
    # ---------------------------------
    def classify(row):

        a = row["CL31 Finish"]
        b = row["CL32 Finish"]

        if pd.notna(a) and pd.isna(b):
            return "REMOVED"

        if pd.isna(a) and pd.notna(b):
            return "NEW"

        if pd.notna(a) and pd.notna(b):

            delta = (b - a).days

            if delta > 0:
                return "DELAYED"

            elif delta < 0:
                return "ACCELERATED"

            else:
                return "UNCHANGED"

        return "UNKNOWN"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # ---------------------------------
    # STATUS COMMENT
    # ---------------------------------
    def comment(row):

        c = row["Change Type"]

        if c == "DELAYED":
            return "Shifted later, coordination required"

        if c == "ACCELERATED":
            return "Earlier than CL31 baseline"

        if c == "NEW":
            return "Added in CL32"

        if c == "REMOVED":
            return "Dropped from CL32"

        return "Stable"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    # format dates
    merged["CL31 Finish"] = merged["CL31 Finish"].apply(format_date)

    merged["CL32 Finish"] = merged["CL32 Finish"].apply(format_date)

    # sort
    merged = merged.sort_values(
        by=["Change Type", "Deliverable"]
    )

    # final columns
    merged = merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return merged.reset_index(drop=True)