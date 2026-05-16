import pandas as pd


def build_deliverable_summary(df):

    # Ensure valid deliverable rows only
    df = df.copy()
    df = df.dropna(subset=["Deliverable"])

    # Group at deliverable level
    summary = (
        df.groupby("Deliverable", as_index=False)["Finish"]
        .max()
    )

    return summary