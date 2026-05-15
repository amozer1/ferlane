import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_schedule():
    cl31_path = DATA_DIR / "CL31.xlsx"
    cl32_path = DATA_DIR / "CL32.xlsx"

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    return cl31, cl32