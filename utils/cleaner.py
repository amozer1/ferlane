import pandas as pd


def clean_programme(df):

    # ============================================
    # STANDARDISE COLUMN NAMES
    # ============================================

    df.columns = df.columns.str.strip()

    # ============================================
    # REMOVE BLANK ACTIVITY IDS
    # ============================================

    df = df[df["Activity ID"].notna()]

    # ============================================
    # REMOVE SUMMARY ROWS
    # ============================================

    df = df[
        ~df["Activity ID"].astype(str).str.contains(
            "Level|Duration",
            case=False,
            na=False
        )
    ]

    # ============================================
    # DATE COLUMNS
    # ============================================

    date_cols = [
        "Start",
        "Finish",
        "BL Project Start",
        "BL Project Finish"
    ]

    for col in date_cols:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.replace("A", "", regex=False)
                .str.replace("*", "", regex=False)
                .str.strip()
            )

            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst=True
            )

    # ============================================
    # NUMERIC COLUMNS
    # ============================================

    numeric_cols = [
        "Remaining Duration",
        "Total Float",
        "Variance - BL Project Finish Date"
    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df