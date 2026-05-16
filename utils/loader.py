import pandas as pd
import re


def clean_date(val):
    if pd.isna(val):
        return pd.NaT

    val = str(val)

    # ----------------------------
    # STEP 1: REMOVE COMMON MS PROJECT JUNK
    # ----------------------------
    val = val.replace("*", "")
    val = re.sub(r"\bA\b", "", val)   # removes standalone A
    val = re.sub(r"\s+", " ", val).strip()

    # ----------------------------
    # STEP 2: EXTRACT ONLY DATE PATTERN
    # (handles: 16-Feb-26, 16-Feb-2026)
    # ----------------------------
    match = re.search(r"\d{1,2}-[A-Za-z]{3}-\d{2,4}", val)

    if not match:
        return pd.NaT

    clean = match.group(0)

    # ----------------------------
    # STEP 3: PARSE STRICTLY
    # ----------------------------
    dt = pd.to_datetime(clean, errors="coerce", dayfirst=True)

    return dt