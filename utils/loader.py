import pandas as pd
import numpy as np
import re


def clean_date(value):
    """
    Cleans Primavera-style dates:
    - Removes 'A' (Actual)
    - Removes '*'' (Constraint)
    - Returns clean datetime
    """
    if pd.isna(value):
        return None

    value = str(value)
    value = value.replace('A', '').replace('*', '').strip()

    try:
        return pd.to_datetime(value, errors='coerce', dayfirst=True)
    except:
        return None


def detect_type(value):
    if pd.isna(value):
        return "Forecast"
    value = str(value)
    if 'A' in value:
        return "Actual"
    if '*' in value:
        return "Constraint"
    return "Forecast"


def load_programme_data(file):
    """Load CL programme file (CSV or Excel)"""

    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    return df


def prepare_comparison_df(df31, df32):
    """
    Build CL31 vs CL32 comparison table
    """

    # Standardise column names
    df31 = df31.copy()
    df32 = df32.copy()

    df31.columns = [c.strip() for c in df31.columns]
    df32.columns = [c.strip() for c in df32.columns]

    # Key mapping assumption
    key_col = "Activity Name"

    # Extract deliverable level rows (filter out empty or group headers)
    df31 = df31[df31[key_col].notna()]
    df32 = df32[df32[key_col].notna()]

    # Build base
    merged = pd.DataFrame()
    merged["Deliverable"] = pd.concat([df31[key_col], df32[key_col]]).drop_duplicates()

    # Map CL31
    df31_map = df31.set_index(key_col)
    df32_map = df32.set_index(key_col)

    def get_val(df, col):
        return merged["Deliverable"].map(lambda x: df[col].get(x, None) if col in df.columns else None)

    # Try to locate finish columns flexibly
    def find_finish_col(df):
        for c in df.columns:
            if "Finish" in c:
                return c
        return None

    c31 = find_finish_col(df31)
    c32 = find_finish_col(df32)

    merged["CL31 Finish"] = merged["Deliverable"].map(df31_map[c31]) if c31 else None
    merged["CL32 Finish"] = merged["Deliverable"].map(df32_map[c32]) if c32 else None

    # Clean dates
    merged["CL31 Clean"] = merged["CL31 Finish"].apply(clean_date)
    merged["CL32 Clean"] = merged["CL32 Finish"].apply(clean_date)

    # Delta
    merged["Delta (Days)"] = (merged["CL32 Clean"] - merged["CL31 Clean"]).dt.days

    # Format delta
    merged["Delta (Days)"] = merged["Delta (Days)"].apply(
        lambda x: f"+{int(x)}" if pd.notna(x) and x > 0 else (
            f"{int(x)}" if pd.notna(x) else "0"
        )
    )

    # Status
    def status(row):
        try:
            d = row["CL32 Clean"] - row["CL31 Clean"]
            if pd.isna(d):
                return "No Data"
            if d.days > 30:
                return "Major Slippage"
            if d.days > 10:
                return "Minor Delay"
            if d.days == 0:
                return "Maintained"
            return "Minor Change"
        except:
            return "No Data"

    merged["Status / Comment"] = merged.apply(status, axis=1)

    # Final format
    return merged[["Deliverable", "CL31 Finish", "CL32 Finish", "Delta (Days)", "Status / Comment"]]
