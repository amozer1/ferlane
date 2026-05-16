import pandas as pd

def load_cl31(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()

    # standardise key fields
    if "Activity ID" not in df.columns:
        raise ValueError("CL31 missing 'Activity ID' column")

    return df


def load_cl32(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    df.columns = df.columns.str.strip()

    if "Activity ID" not in df.columns:
        raise ValueError("CL32 missing 'Activity ID' column")

    return df