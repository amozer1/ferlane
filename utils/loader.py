import pandas as pd
import numpy as np
import re

DATE_FMT = "%d-%b-%Y"


def clean_date(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()
    value = re.sub(r"[A*]", "", value).strip()

    if value == "":
        return np.nan

    return pd.to_datetime(value, dayfirst=True, errors="coerce")


def format_date(value):
    if pd.isna(value):
        return None
    return value.strftime(DATE_FMT)


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


def fill_dates(df):
    # fallback logic (NO blanks allowed)
    df["Start"] = df["Start"].combine_first(df["BL Start"])
    df["BL Start"] = df["BL Start"].combine_first(df["Start"])

    df["Finish"] = df["Finish"].combine_first(df["BL Finish"])
    df["BL Finish"] = df["BL Finish"].combine_first(df["Finish"])

    for c in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[c] = df[c].apply(clean_date)

    # HARD RULE: remove rows still missing dates
    df = df.dropna(subset=["Start", "Finish", "BL Finish"])

    for c in ["Start", "Finish", "BL Start", "BL Finish"]:
        df[c] = df[c].apply(format_date)

    return df


def load_programme(path):
    df = pd.read_excel(path)
    df = standardise(df)
    df = fill_dates(df)
    return df