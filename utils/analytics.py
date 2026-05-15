# utils/analytics.py

import pandas as pd

def compute_kpis(df: pd.DataFrame):
    df = df.copy()

    if "Float" not in df.columns:
        df["Float"] = 0

    if "Status" not in df.columns:
        df["Status"] = "Unknown"

    return {
        "total": len(df),
        "avg_float": df["Float"].mean(),
        "critical": (df["Status"] == "Critical").sum(),
        "near_critical": (df["Status"] == "Near Critical").sum(),
        "non_critical": (df["Status"] == "Non Critical").sum(),
    }