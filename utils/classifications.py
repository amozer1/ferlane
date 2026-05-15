import pandas as pd
import numpy as np

def classify_status(delta):

    if pd.isna(delta):
        return "Unknown"

    if delta > 0:
        return "Delayed"

    elif delta < 0:
        return "Accelerated"

    return "On Track"


def apply_classification(df):

    df["status"] = df["delta_finish"].apply(classify_status)

    if "total float_32" in df.columns:

        df["critical"] = np.where(
            df["total float_32"] < 0,
            "Critical",
            "Normal"
        )

    else:

        df["critical"] = "Unknown"

    return df