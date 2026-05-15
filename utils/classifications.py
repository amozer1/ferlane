import numpy as np

def classify_status(delta):
    if delta > 0:
        return "Delayed"
    elif delta < 0:
        return "Accelerated"
    return "On Track"


def apply_status(df):
    df["status"] = df["delta_finish"].apply(classify_status)

    df["critical"] = np.where(
        df["delta_finish"] > 10,
        "Critical",
        "Normal"
    )
    return df