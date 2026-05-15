import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_programme_data():

    cl31_path = DATA_DIR / "CL31.xlsx"
    cl32_path = DATA_DIR / "CL32.xlsx"

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    # standardisation (critical for NEC consistency)
    required_cols = ["Activity", "Start", "Finish"]

    for col in required_cols:
        if col not in cl32.columns:
            cl32[col] = None
        if col not in cl31.columns:
            cl31[col] = None

    return cl31, cl32