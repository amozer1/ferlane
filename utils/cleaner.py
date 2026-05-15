import pandas as pd

def clean_primavera(df):

    # Standardise columns
    df.columns = df.columns.str.strip().str.lower()

    # Remove blank activity ids
    df = df[df["activity id"].notna()]

    # Keep real activities only
    df = df[
        df["activity id"]
        .astype(str)
        .str.contains("AMP8|CE-", na=False)
    ]

    # Clean dates
    def clean_dates(series):

        return pd.to_datetime(
            series.astype(str)
            .str.replace("A", "", regex=False)
            .str.replace("*", "", regex=False)
            .str.strip(),
            errors="coerce"
        )

    for col in ["start", "finish"]:

        if col in df.columns:
            df[col] = clean_dates(df[col])

    # Float conversion
    if "total float" in df.columns:

        df["total float"] = pd.to_numeric(
            df["total float"],
            errors="coerce"
        )

    return df