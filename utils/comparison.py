import pandas as pd


def compare_programmes(df31, df32):

    merged = pd.merge(
        df31,
        df32,
        on="Activity ID",
        how="outer",
        suffixes=("_31", "_32")
    )

    return merged