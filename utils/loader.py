import pandas as pd
import numpy as np
import re


# ----------------------------
# CLEAN DATE FUNCTION
# ----------------------------
def clean_date(val):
    if pd.isna(val):
        return np.nan

    val = str(val).strip()

    # remove A, *, trailing spaces
    val = re.sub(r"[A\*]", "", val).strip()

    return pd.to_datetime(val, errors="coerce", dayfirst=True)


# ----------------------------
# DISCIPLINE CLASSIFIER
# ----------------------------
def classify_discipline(name):
    name = str(name).lower()

    if any(x in name for x in ["civ", "shaft", "pipe", "mh", "benching", "slab"]):
        return "Civils / Structural"

    if any(x in name for x in ["mechanical", "pump", "ga drawing", "rising", "mec"]):
        return "Mechanical"

    if any(x in name for x in ["eica", "electrical", "instrument", "telemetry", "dno"]):
        return "EICA"

    if any(x in name for x in ["process", "hazop", "p&id", "control"]):
        return "Process"

    if any(x in name for x in ["geo", "geotechnical", "gdr"]):
        return "Geotechnical"

    return "Other"


# ----------------------------
# LOAD AND NORMALISE FILE
# ----------------------------
def load_programme(file):

    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]

    # find deliverable + finish column
    deliverable_col = "Activity Name"
    finish_col = [c for c in df.columns if "Finish" in c][-1]

    df = df[[deliverable_col, finish_col]].copy()
    df.columns = ["Deliverable", "Finish"]

    df["Deliverable"] = df["Deliverable"].astype(str).str.strip()
    df["Finish"] = df["Finish"].apply(clean_date)

    # REMOVE blank finish rows (your requirement)
    df = df[df["Finish"].notna()]

    # REMOVE duplicates (CRITICAL FIX)
    df = df.drop_duplicates(subset=["Deliverable"], keep="last")

    return df


# ----------------------------
# MAIN COMPARISON ENGINE
# ----------------------------
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

    # ----------------------------
    # CHANGE TYPE
    # ----------------------------
    def change_type(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        if row["CL31 Finish"] != row["CL32 Finish"]:
            return "DELAYED"
        return "UNCHANGED"


    merged["Change Type"] = merged.apply(change_type, axis=1)

    # ----------------------------
    # DELTA
    # ----------------------------
    def delta(row):
        if pd.isna(row["CL31 Finish"]) or pd.isna(row["CL32 Finish"]):
            return np.nan
        return (row["CL32 Finish"] - row["CL31 Finish"]).days


    merged["Delta (Days)"] = merged.apply(delta, axis=1)


    # ----------------------------
    # COMMENTS
    # ----------------------------
    def comment(row):
        if row["Change Type"] == "NEW":
            return "Added in CL32"
        if row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        if row["Change Type"] == "DELAYED":
            return "Shifted vs CL31 baseline"
        return "No change"


    merged["Status / Comment"] = merged.apply(comment, axis=1)

    # ----------------------------
    # DISCIPLINE
    # ----------------------------
    merged["Discipline"] = merged["Deliverable"].apply(classify_discipline)

    # ----------------------------
    # FORMAT DATES (FINAL UI FORMAT)
    # ----------------------------
    for col in ["CL31 Finish", "CL32 Finish"]:
        merged[col] = merged[col].dt.strftime("%d-%b-%Y")

    # ----------------------------
    # FINAL ORDER
    # ----------------------------
    merged = merged[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Change Type",
            "Status / Comment",
            "Discipline"
        ]
    ]

    return merged