import pandas as pd


def clean_primavera(df):

    df.columns = df.columns.str.strip().str.lower()

    df = df[df["activity id"].notna()]

    df = df[
        df["activity id"]
        .astype(str)
        .str.contains("AMP8|CE-", na=False)
    ]

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

    if "total float" in df.columns:

        df["total float"] = pd.to_numeric(
            df["total float"],
            errors="coerce"
        )

    return df