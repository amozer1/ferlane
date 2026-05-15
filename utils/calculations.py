import numpy as np


def calculate_deltas(df):

    df["delta_start_days"] = (
        df["start_32"] - df["start_31"]
    ).dt.days

    df["delta_finish_days"] = (
        df["finish_32"] - df["finish_31"]
    ).dt.days

    df["float_band"] = np.select(
        [
            df["total float_32"] < 0,
            (df["total float_32"] >= 0) & (df["total float_32"] <= 10),
            (df["total float_32"] > 10) & (df["total float_32"] <= 20),
            (df["total float_32"] > 20)
        ],
        [
            "Critical",
            "Near Critical",
            "Low Float",
            "Non Critical"
        ],
        default="Unknown"
    )

    return df