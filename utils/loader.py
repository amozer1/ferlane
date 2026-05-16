import pandas as pd


def clean_dates(df):
    date_cols = [
        "Start",
        "Finish",
        "BL1 Start",
        "BL1 Finish"
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
                format="%d-%b-%y",
                errors="coerce"
            )

    return df


def load_programme(path):
    df = pd.read_excel(path)

    df.columns = [c.strip() for c in df.columns]

    required = [
        "Activity Name",
        "Finish",
        "BL1 Finish",
        "Total Float"
    ]

    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")

    df = clean_dates(df)

    df["Activity Name"] = (
        df["Activity Name"]
        .astype(str)
        .str.strip()
    )

    df["Total Float"] = pd.to_numeric(
        df["Total Float"],
        errors="coerce"
    )

    return df