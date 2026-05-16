# =========================
# utils/loader.py
# =========================

import pandas as pd


def clean_columns(df):
    df.columns = [str(c).strip() for c in df.columns]
    return df


def load_schedule(cl31_path, cl32_path):

    # -------------------------
    # LOAD EXCEL FILES
    # -------------------------
    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    # -------------------------
    # CLEAN COLUMNS
    # -------------------------
    cl31 = clean_columns(cl31)
    cl32 = clean_columns(cl32)

    # -------------------------
    # DATE CONVERSION
    # -------------------------
    for col in ["Start", "Finish", "BL1 Start", "BL1 Finish"]:
        if col in cl31.columns:
            cl31[col] = pd.to_datetime(cl31[col], errors="coerce")

        if col in cl32.columns:
            cl32[col] = pd.to_datetime(cl32[col], errors="coerce")

    return cl31, cl32