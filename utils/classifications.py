# utils/classifications.py

import pandas as pd

def classify_float(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Float" not in df.columns:
        df["Float"] = 0

    def classify(f):
        if f <= 0:
            return "Critical"
        elif f <= 5:
            return "Near Critical"
        else:
            return "Non Critical"

    df["Status"] = df["Float"].apply(classify)

    return df