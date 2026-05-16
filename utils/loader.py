# =========================
# utils/loader.py
# =========================

import pandas as pd


def clean_columns(df):

    df.columns = [str(c).strip() for c in df.columns]

    return df


def clean_dates(df):

    date_columns = [
        "Start",
        "Finish",
        "BL1 Start",
        "BL1 Finish"
    ]

    for col in date_columns:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce"
            )

    return df


def clean_float(df):

    if "Total Float" in df.columns:

        df["Total Float"] = pd.to_numeric(
            df["Total Float"],
            errors="coerce"
        ).fillna(0)

    return df


def load_schedule(cl31_path, cl32_path):

    # ---------------------------------------------------
    # LOAD FILES
    # ---------------------------------------------------

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    # ---------------------------------------------------
    # CLEAN
    # ---------------------------------------------------

    cl31 = clean_columns(cl31)
    cl32 = clean_columns(cl32)

    cl31 = clean_dates(cl31)
    cl32 = clean_dates(cl32)

    cl31 = clean_float(cl31)
    cl32 = clean_float(cl32)

    # ---------------------------------------------------
    # REMOVE EMPTY ACTIVITY NAMES
    # ---------------------------------------------------

    cl31 = cl31.dropna(subset=["Activity Name"])
    cl32 = cl32.dropna(subset=["Activity Name"])

    return cl31, cl32