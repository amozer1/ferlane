# loader.py
import pandas as pd
from pathlib import Path

DATA_PATH = Path("data")

CL31_FILE = DATA_PATH / "CL31-February.xlsx"
CL32_FILE = DATA_PATH / "CL32-May.xlsx"


def load_excel(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing file: {file_path}")
    return pd.read_excel(file_path)


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]
    return df


def flatten_schedule(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_columns(df)

    rename_map = {
        "Activity Name": "name",
        "Finish": "finish",
        "Start": "start",
        "Activity ID": "id"
    }

    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    if "name" not in df.columns:
        raise ValueError("Missing 'Activity Name' column in file")

    df = df[df["name"].notna()].copy()

    return df


def load_programmes():
    cl31 = flatten_schedule(load_excel(CL31_FILE))
    cl32 = flatten_schedule(load_excel(CL32_FILE))
    return cl31, cl32