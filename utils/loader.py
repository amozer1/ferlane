# utils/loader.py
import pandas as pd

def clean_df(df):
    df.columns = df.columns.str.strip()

    if "Activity ID" in df.columns:
        df["Activity ID"] = df["Activity ID"].astype(str).str.strip().str.upper()

    date_cols = [c for c in df.columns if "Finish" in c or "Date" in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def load_cl31(path):
    df = pd.read_excel(path, engine="openpyxl")
    df = clean_df(df)

    df = df.rename(columns={
        "Finish": "CL31 Finish",
        "Activity Name": "Activity Name_CL31"
    })

    return df


def load_cl32(path):
    df = pd.read_excel(path, engine="openpyxl")
    df = clean_df(df)

    df = df.rename(columns={
        "Finish": "CL32 Finish",
        "Activity Name": "Activity Name_CL32"
    })

    return df