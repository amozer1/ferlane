import pandas as pd
import os

def load_programmes(file_path: str) -> pd.DataFrame:
    """
    Loads CL31 / CL32 programme data safely.
    """

    # 🔴 Hard fail if file missing (prevents silent Streamlit errors)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as e:
        raise RuntimeError(f"Failed to read Excel file: {file_path}. Error: {e}")

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]

    return df