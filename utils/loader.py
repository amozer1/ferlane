import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")


def load_cl31():
    file_path = DATA_PATH / "CL31-February.xlsx"
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df


def load_cl32():
    file_path = DATA_PATH / "CL32-May.xlsx"
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    return df