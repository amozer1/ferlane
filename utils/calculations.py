def calculate_deltas(df):

    df["delta_start"] = (
        df["start_32"] - df["start_31"]
    ).dt.days

    df["delta_finish"] = (
        df["finish_32"] - df["finish_31"]
    ).dt.days

    return df