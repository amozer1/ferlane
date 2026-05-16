import pandas as pd
import numpy as np


def _clean_columns(df):
    df.columns = [c.strip() for c in df.columns]
    return df


# ---------- SMART DATE PARSER ----------
def parse_mixed_date(value):
    """
    Handles:
    - 2026-06-12T00:00:00
    - 12-Jun-26
    - 12/06/2026
    - 16-Feb-26 A
    - Excel blanks / NaN
    """

    if pd.isna(value):
        return pd.NaT

    if isinstance(value, str):
        value = value.strip()

        # remove trailing status like "A"
        value = value.replace(" A", "").replace("*", "")

        if value == "" or value.lower() in ["nan", "none", "—", "-"]:
            return pd.NaT

    return pd.to_datetime(value, errors="coerce", dayfirst=True)


def _parse_all_dates(df):
    date_cols = [c for c in df.columns if "Start" in c or "Finish" in c]

    for col in date_cols:
        df[col] = df[col].apply(parse_mixed_date)

    return df


def load_programmes(file_path):
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    df = _clean_columns(df)
    df = _parse_all_dates(df)

    return df