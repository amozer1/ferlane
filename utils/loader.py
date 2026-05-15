# utils/loader.py

import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

def load_programme_data():
    """
    Loads CL31 and CL32 Excel files and standardises column names.
    Ensures required fields exist for downstream analytics.
    """

    cl31_path = DATA_DIR / "CL31.xlsx"
    cl32_path = DATA_DIR / "CL32.xlsx"

    cl31 = pd.read_excel(cl31_path)
    cl32 = pd.read_excel(cl32_path)

    # -----------------------------
    # STANDARDISE COLUMN NAMES
    # -----------------------------
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # Strip whitespace
        df.columns = [c.strip() for c in df.columns]

        # Map known variations → standard names
        rename_map = {
            "Total Float": "Float",
            "TOTAL FLOAT": "Float",
            "total float": "Float",
            "Finish Date": "Finish",
            "Finish": "Finish",
        }

        df.rename(columns=rename_map, inplace=True)

        # Ensure Float exists
        if "Float" not in df.columns:
            df["Float"] = 0

        # Convert Float safely
        df["Float"] = pd.to_numeric(df["Float"], errors="coerce").fillna(0)

        # Ensure Finish exists (optional safety)
        if "Finish" not in df.columns:
            df["Finish"] = pd.NaT

        return df

    cl31 = clean(cl31)
    cl32 = clean(cl32)

    return cl31, cl32