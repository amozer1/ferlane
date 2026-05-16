# utils/loader.py

import pandas as pd


def _to_date(series):
    return pd.to_datetime(series, errors="coerce")


def load_programme(file):
    df = pd.read_excel(file)
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(how="all")

    if "Activity Name" not in df.columns:
        raise ValueError("Missing column: Activity Name")

    df = df[df["Activity Name"].notna()]
    df["Activity Name"] = df["Activity Name"].astype(str).str.strip()

    # -----------------------------
    # SAFE COLUMN PICKING
    # -----------------------------
    def col(name):
        return df[name] if name in df.columns else pd.Series([pd.NA] * len(df))

    start = _to_date(col("Start"))
    finish = _to_date(col("Finish"))

    # CL32 baseline
    bl1_start = _to_date(col("BL1 Start"))
    bl1_finish = _to_date(col("BL1 Finish"))

    # CL31 baseline
    blp_start = _to_date(col("BL Project Start"))
    blp_finish = _to_date(col("BL Project Finish"))

    # -----------------------------
    # UNIFIED FALLBACK LOGIC
    # -----------------------------
    df["Start_Eff"] = start.fillna(bl1_start).fillna(blp_start)
    df["Finish_Eff"] = finish.fillna(bl1_finish).fillna(blp_finish)

    # Drop rows still missing BOTH
    df = df.dropna(subset=["Start_Eff", "Finish_Eff"], how="any")

    return df