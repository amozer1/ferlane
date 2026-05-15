import pandas as pd


def merge_programmes(df31, df32):

    df = pd.merge(
        df31,
        df32,
        on="activity id",
        how="outer",
        suffixes=("_31", "_32")
    )

    return df