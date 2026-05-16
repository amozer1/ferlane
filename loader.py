import pandas as pd
import numpy as np

# =========================
# COLUMN NORMALISATION MAP
# =========================
COLUMN_MAP = {
    "Activity Name": "Activity Name",

    "Start": "Start",
    "Finish": "Finish",

    # CL31 format
    "BL Project Start": "BL Start",
    "BL Project Finish": "BL Finish",

    # CL32 format
    "BL1 Start": "BL Start",
    "BL1 Finish": "BL Finish",

    # fallback variants
    "Baseline Start": "BL Start",
    "Baseline Finish": "BL Finish",
}


DATE_COLS = ["Start", "Finish", "BL Start", "BL Finish"]


# -------------------------
# CLEAN HEADERS
# -------------------------
def _clean_columns(df):
    df.columns = df.columns.str.strip()
    df = df.rename(columns=lambda x: COLUMN_MAP.get(x, x))
    return df


# -------------------------
# CLEAN TEXT
# -------------------------
def _clean_text(val):
    if pd.isna(val):
        return np.nan
    return str(val).replace(" A", "").strip()


# -------------------------
# DATE PARSER (CRITICAL FIX)
# -------------------------
def _parse_date(val):
    if pd.isna(val) or val == "":
        return np.nan

    val = str(val).replace(" A", "").strip()

    return pd.to_datetime(val, errors="coerce", dayfirst=True)


# -------------------------
# MAIN LOADER
# -------------------------
def load_schedule(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)

    # standardise headers
    df = _clean_columns(df)

    # clean activity names
    if "Activity Name" in df.columns:
        df["Activity Name"] = df["Activity Name"].apply(_clean_text)

    # parse all known date fields
    for col in DATE_COLS:
        if col in df.columns:
            df[col] = df[col].apply(_parse_date)

    return df