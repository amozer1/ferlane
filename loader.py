import pandas as pd


def clean_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.replace("\n", " ")
        .str.strip()
    )
    return df


def parse_dates(df, col):
    df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    return df


def load_cl31(path="data/CL31-February.xlsx"):
    df = pd.read_excel(path)
    df = clean_columns(df)

    df = df[["Activity Name", "BL Project Finish"]]
    df = parse_dates(df, "BL Project Finish")

    return df


def load_cl32(path="data/CL32-May.xlsx"):
    df = pd.read_excel(path)
    df = clean_columns(df)

    df = df[["Activity Name", "Finish"]]
    df = parse_dates(df, "Finish")

    return df