import pandas as pd

def build_variance_table(cl31, cl32):
    df = cl31.merge(
        cl32,
        on="Activity ID",
        suffixes=("_cl31", "_cl32")
    )

    df["Deliverable"] = df["Activity Name"]

    df["CL31 Finish"] = df["Finish_cl31"]
    df["CL32 Finish"] = df["Finish_cl32"]

    return df