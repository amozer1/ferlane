import pandas as pd

def _clean_columns(df):
    df.columns = (
        df.columns
        .astype(str)
        .str.replace("\n", " ")
        .str.replace("\t", " ")
        .str.strip()
    )
    return df


def _parse_dates(series):
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


# =========================
# CL31 LOADER
# =========================
def load_cl31(path="data/CL31-February.xlsx"):
    df = pd.read_excel(path)
    df = _clean_columns(df)

    # Ensure required columns exist
    required = ["Activity Name", "BL Project Finish"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    df = df[["Activity Name", "BL Project Finish"]]

    df["BL Project Finish"] = _parse_dates(df["BL Project Finish"])

    return df


# =========================
# CL32 LOADER
# =========================
def load_cl32(path="data/CL32-May.xlsx"):
    df = pd.read_excel(path)
    df = _clean_columns(df)

    required = ["Activity Name", "Finish"]
    for col in required:
        if col not in df.columns:
            df[col] = None

    df = df[["Activity Name", "Finish"]]

    df["Finish"] = _parse_dates(df["Finish"])

    return df