import pandas as pd

def calc_deltas(df):
    df["delta_start"] = (df["clause 32 start"] - df["clause 31 start"]).dt.days
    df["delta_finish"] = (df["clause 32 finish"] - df["clause 31 finish"]).dt.days
    return df