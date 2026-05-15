import pandas as pd

def calculate_delta(row):
    return (row["CL32 Finish"] - row["CL31 Finish"]).days


def calculate_float_change(row):
    return row["Total Float_cl32"] - row["Total Float_cl31"]