import pandas as pd


def _load_excel(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)

    # Clean column names (fixes KeyError issues)
    df.columns = df.columns.str.strip()

    return df


def _standardise_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures all schedule date fields are proper datetime.
    Safe conversion for CL31/CL32 exports.
    """

    date_columns = [
        "Start",
        "Finish",
        "BL1 Start",
        "BL1 Finish"
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def load_cl31(path="data/CL31-February.xlsx"):
    df = _load_excel(path)
    return _standardise_dates(df)


def load_cl32(path="data/CL32-May.xlsx"):
    df = _load_excel(path)
    return _standardise_dates(df)