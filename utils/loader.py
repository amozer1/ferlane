import pandas as pd


def load_programme(file_path):
    """
    Robust loader for CL31 / CL32 Excel files
    - No strict column enforcement
    - Cleans headers
    - Handles P6 / Excel export inconsistencies
    """

    df = pd.read_excel(file_path, engine="openpyxl")

    # -----------------------------
    # CLEAN COLUMN HEADERS
    # -----------------------------
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ")
    )

    # -----------------------------
    # BASIC VALIDATION ONLY
    # -----------------------------
    if "Activity Name" not in df.columns:
        raise ValueError(
            "Missing required column: 'Activity Name'. "
            "Check Excel export format."
        )

    # -----------------------------
    # OPTIONAL CLEANING
    # -----------------------------
    df = df.copy()

    # remove fully empty rows
    df = df.dropna(how="all")

    # ensure Activity Name is usable
    df = df[df["Activity Name"].notna()]

    return df