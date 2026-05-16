# utils/loader.py

import pandas as pd
import re


def clean_date(val):
    if pd.isna(val):
        return pd.NaT

    val = str(val)

    # remove MS Project junk
    val = val.replace("*", "")
    val = re.sub(r"\bA\b", "", val)
    val = re.sub(r"\s+", " ", val).strip()

    # extract valid date pattern
    match = re.search(r"\d{1,2}-[A-Za-z]{3}-\d{2,4}", val)

    if not match:
        return pd.NaT

    return pd.to_datetime(match.group(0), errors="coerce", dayfirst=True)


def load_programme(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]

    df = df.dropna(how="all")

    if "Activity Name" not in df.columns:
        raise ValueError("Missing column: Activity Name")

    df = df[df["Activity Name"].notna()]
    df["Activity Name"] = df["Activity Name"].astype(str).str.strip()

    def col(name):
        return df[name] if name in df.columns else pd.Series([pd.NA] * len(df))

    start = col("Start").apply(clean_date)
    finish = col("Finish").apply(clean_date)

    bl1_start = col("BL1 Start").apply(clean_date)
    bl1_finish = col("BL1 Finish").apply(clean_date)

    blp_start = col("BL Project Start").apply(clean_date)
    blp_finish = col("BL Project Finish").apply(clean_date)

    # fallback logic
    df["Start_Eff"] = start.fillna(bl1_start).fillna(blp_start)
    df["Finish_Eff"] = finish.fillna(bl1_finish).fillna(blp_finish)

    # HARD CLEAN RULE
    df = df.dropna(subset=["Start_Eff", "Finish_Eff"], how="any")

    # standard format
    df["Start_Eff"] = df["Start_Eff"].dt.strftime("%d-%b-%Y")
    df["Finish_Eff"] = df["Finish_Eff"].dt.strftime("%d-%b-%Y")

    return df