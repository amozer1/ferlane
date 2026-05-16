import pandas as pd
import numpy as np
import re

DATE_FMT = "%d-%b-%Y"


# -------------------------
# CLEAN RAW DATE STRING
# -------------------------
def clean_date(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # remove A, *, extra spaces
    value = re.sub(r"[A*]", "", value).strip()

    if value == "" or value.lower() == "nan":
        return np.nan

    return value  # KEEP AS STRING FIRST (IMPORTANT FIX)


# -------------------------
# SAFE PARSE AFTER CLEANING
# -------------------------
def parse_date(value):
    if pd.isna(value):
        return np.nan

    try:
        return pd.to_datetime(value, dayfirst=True, errors="coerce")
    except:
        return np.nan


# -------------------------
# FORMAT OUTPUT
# -------------------------
def format_date(value):
    if pd.isna(value):
        return None
    return value.strftime(DATE_FMT)


# -------------------------
# STANDARDISE COLUMNS
# -------------------------
def standardise(df):

    cols = {c.lower().strip(): c for c in df.columns}

    def pick(*keys):
        for k in keys:
            if k in cols:
                return cols[k]
        return None

    return pd.DataFrame({
        "Activity Name": df[pick("activity name")],
        "Start": df[pick("start")],
        "Finish": df[pick("finish")],
        "BL Start": df[pick("bl1 start", "bl project start")],
        "BL Finish": df[pick("bl1 finish", "bl project finish")]
    })


# -------------------------
# FIX DATE FALLBACK (SAFE)
# -------------------------
def fill_dates(df):

    # STEP 1: CLEAN ALL RAW VALUES FIRST
    for col in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[col] = df[col].apply(clean_date)

    # STEP 2: SAFE FALLBACK (STRING LEVEL ONLY)
    df["Start"] = df["Start"].fillna(df["BL Start"])
    df["BL Start"] = df["BL Start"].fillna(df["Start"])

    df["Finish"] = df["Finish"].fillna(df["BL Finish"])
    df["BL Finish"] = df["BL Finish"].fillna(df["Finish"])

    # STEP 3: NOW PARSE SAFELY
    for col in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[col] = df[col].apply(parse_date)

    # STEP 4: DROP ONLY TRUE INVALID ROWS
    df = df.dropna(subset=["Start", "Finish"])

    # STEP 5: FORMAT FINAL OUTPUT
    for col in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[col] = df[col].apply(format_date)

    return df


# -------------------------
# MAIN LOADER
# -------------------------
def load_programme(path):
    df = pd.read_excel(path)
    df = standardise(df)
    df = fill_dates(df)
    return df