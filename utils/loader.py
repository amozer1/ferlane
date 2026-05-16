import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")


def load_cl31():
    df = pd.read_excel(DATA_PATH / "CL31-February.xlsx")
    df.columns = df.columns.str.strip()
    return df


def load_cl32():
    df = pd.read_excel(DATA_PATH / "CL32-May.xlsx")
    df.columns = df.columns.str.strip()
    return df