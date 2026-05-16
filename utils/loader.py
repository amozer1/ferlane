import pandas as pd

def _load_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    # Clean column names (THIS FIXES your KeyError issues)
    df.columns = df.columns.str.strip()

    return df


def load_cl31(path="data/CL31-February.xlsx"):
    return _load_excel(path)


def load_cl32(path="data/CL32-May.xlsx"):
    return _load_excel(path)