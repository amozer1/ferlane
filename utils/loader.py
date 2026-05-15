import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_schedule():
    cl31_path = DATA_DIR / "CL31.xlsx"
    cl32_path = DATA_DIR / "CL32.xlsx"

    if not cl31_path.exists():
        raise FileNotFoundError(f"Missing file: {cl31_path}")

    if not cl32_path.exists():
        raise FileNotFoundError(f"Missing file: {cl32_path}")

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    return cl31, cl32