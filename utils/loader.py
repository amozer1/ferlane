import pandas as pd
import numpy as np
import re

DATE_FMT = "%d-%b-%Y"


def clean_date(value):
    """Remove A, *, whitespace and parse date safely"""
    if pd.isna(value):
        return np.nan

    value = str(value).strip()

    # remove A, *, extra spaces
    value = re.sub(r"[A*]", "", value).strip()

    if value == "" or value.lower() == "nan":
        return np.nan

    try:
        return pd.to_datetime(value, dayfirst=True, errors="coerce")
    except:
        return np.nan


def format_date(value):
    if pd.isna(value):
        return None
    return value.strftime(DATE_FMT)


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Unify CL31 and CL32 column names"""

    cols = {c.lower().strip(): c for c in df.columns}

    def find(*keys):
        for k in keys:
            if k in cols:
                return cols[k]
        return None

    start = find("start")
    finish = find("finish")

    bl_start = find("bl1 start", "bl project start", "baseline start")
    bl_finish = find("bl1 finish", "bl project finish", "baseline finish")

    activity = find("activity name")

    out = pd.DataFrame()
    out["Activity Name"] = df[activity]

    out["Start"] = df[start] if start else np.nan
    out["Finish"] = df[finish] if finish else np.nan
    out["BL Start"] = df[bl_start] if bl_start else np.nan
    out["BL Finish"] = df[bl_finish] if bl_finish else np.nan

    return out


def fill_missing_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fallback logic:
    Start ↔ BL Start
    Finish ↔ BL Finish
    """

    df["Start"] = df["Start"].combine_first(df["BL Start"])
    df["BL Start"] = df["BL Start"].combine_first(df["Start"])

    df["Finish"] = df["Finish"].combine_first(df["BL Finish"])
    df["BL Finish"] = df["BL Finish"].combine_first(df["Finish"])

    # final cleanup parsing
    for col in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[col] = df[col].apply(clean_date)

    # drop ONLY if still missing critical dates
    df = df.dropna(subset=["Start", "Finish"])

    # format dates
    for col in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[col] = df[col].apply(format_date)

    return df


def load_programme(file) -> pd.DataFrame:
    df = pd.read_excel(file)

    df = standardise_columns(df)
    df = fill_missing_dates(df)

    return df