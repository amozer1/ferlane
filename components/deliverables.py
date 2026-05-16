import pandas as pd


def build_deliverable_summary(df):

    df = df.dropna(subset=["Deliverable"])

    return (
        df.groupby("Deliverable", as_index=False)["Finish"]
        .max()
    )