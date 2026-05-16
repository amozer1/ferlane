import pandas as pd
import os

def load_programmes(file_path: str) -> pd.DataFrame:
    """
    Load CL31 / CL32 Excel safely for Streamlit Cloud.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_excel(file_path, engine="openpyxl")

    df.columns = [str(c).strip() for c in df.columns]

    return df