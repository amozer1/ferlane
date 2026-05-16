# loader.py

import pandas as pd


def _load_excel(path):

    df = pd.read_excel(path)

    # Clean columns
    df.columns = df.columns.str.strip()

    return df


def load_cl31(path="data/CL31-February.xlsx"):

    df = _load_excel(path)
    df["Source"] = "CL31"

    return df


def load_cl32(path="data/CL32-May.xlsx"):

    df = _load_excel(path)
    df["Source"] = "CL32"

    return df