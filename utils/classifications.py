import pandas as pd


def classify_status(delta):

    if pd.isna(delta):
        return "Unknown"

    if delta > 0:
        return "Delayed"

    elif delta < 0:
        return "Accelerated"

    return "On Track"


def apply_classification(df):

    df["status"] = df["delta_finish_days"].apply(classify_status)

    return df