# components/deliverables.py

import pandas as pd


def extract_deliverables(df: pd.DataFrame):
    if "Activity Name" not in df.columns:
        raise ValueError("Missing column: Activity Name")

    df = df.dropna(subset=["Activity Name"])
    df["Activity Name"] = df["Activity Name"].astype(str).str.strip()

    df = df[df["Activity Name"] != ""]

    return df["Activity Name"].drop_duplicates().tolist()