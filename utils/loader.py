# utils/loader.py

import pandas as pd
import re


def clean_date(val):
    """
    Cleans messy MS Project / Excel dates like:
    - 16-Feb-26 A
    - 07-Oct-26*
    - blanks
    """

    if pd.isna(val):
        return pd.NaT

    val = str(val)

    # remove letters like A, *, etc.
    val = re.sub(r"[^\d\-\/A-Za-z ]", "", val)

    # remove trailing letters (A, B, etc.)
    val = re.sub(r"\s+[A-Za-z]+$", "", val)

    # remove extra spaces
    val = val.strip()

    return pd.to_datetime(val, errors="coerce", dayfirst=True)


def load_programme(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]

    df = df.dropna(how="all")

    if "Activity Name" not in df.columns:
        raise ValueError("Missing column: Activity Name")

    df = df[df["Activity Name"].notna()]
    df["Activity Name"] = df["Activity Name"].astype(str).str.strip()

    # -----------------------------
    # SAFE COLUMN ACCESS
    # -----------------------------
    def get(col):
        return df[col] if col in df.columns else pd.Series([pd.NA] * len(df))

    start = get("Start").apply(clean_date)
    finish = get("Finish").apply(clean_date)

    bl1_start = get("BL1 Start").apply(clean_date)
    bl1_finish = get("BL1 Finish").apply(clean_date)

    blp_start = get("BL Project Start").apply(clean_date)
    blp_finish = get("BL Project Finish").apply(clean_date)

    # -----------------------------
    # FALLBACK LOGIC
    # -----------------------------
    df["Start_Eff"] = start.fillna(bl1_start).fillna(blp_start)
    df["Finish_Eff"] = finish.fillna(bl1_finish).fillna(blp_finish)

    # -----------------------------
    # HARD RULE: REMOVE INVALID ROWS
    # -----------------------------
    df = df.dropna(subset=["Start_Eff", "Finish_Eff"], how="any")

    # -----------------------------
    # OPTIONAL: FORMAT CONSISTENCY
    # -----------------------------
    df["Start_Eff"] = df["Start_Eff"].dt.strftime("%d-%b-%Y")
    df["Finish_Eff"] = df["Finish_Eff"].dt.strftime("%d-%b-%Y")

    return df