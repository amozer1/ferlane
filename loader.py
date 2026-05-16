import pandas as pd


def _clean_columns(df):
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )
    return df


def _load(path):
    df = pd.read_excel(path, engine="openpyxl")
    return _clean_columns(df)


def load_cl31(path="data/CL31-February.xlsx"):
    return _load(path)


def load_cl32(path="data/CL32-May.xlsx"):
    return _load(path)