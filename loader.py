import pandas as pd


def _clean_date(series: pd.Series) -> pd.Series:
    """
    Robust date parser:
    - handles blanks
    - handles 'A' suffix
    - handles mixed formats
    """
    series = series.astype(str).str.replace("A", "", regex=False).str.strip()
    series = series.replace(["", "nan", "NaT", "None"], pd.NA)
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def load_cl31(path="data/CL31-February.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Activity Name": "Activity"
    })

    df["Finish"] = _clean_date(df["Finish"])
    df["Start"] = _clean_date(df["Start"])
    df["BL Project Finish"] = _clean_date(df["BL Project Finish"])

    return df


def load_cl32(path="data/CL32-May.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "Activity Name": "Activity"
    })

    df["Finish"] = _clean_date(df["Finish"])
    df["Start"] = _clean_date(df["Start"])
    df["BL1 Finish"] = _clean_date(df["BL1 Finish"])

    return df