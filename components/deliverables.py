import pandas as pd
import numpy as np

def build_deliverables_report(cl31, cl32):

    cl31 = cl31.rename(columns={"Finish": "CL31 Finish"})
    cl32 = cl32.rename(columns={"Finish": "CL32 Finish"})

    df = pd.merge(
        cl31,
        cl32,
        on="Activity",
        how="outer"
    )

    def change_type(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        return "COMPARE"

    df["Change Type"] = df.apply(change_type, axis=1)

    def delta(row):
        if row["Change Type"] != "COMPARE":
            return np.nan
        return (row["CL32 Finish"] - row["CL31 Finish"]).days

    df["Delta (Days)"] = df.apply(delta, axis=1)

    def status(row):
        if row["Change Type"] == "NEW":
            return "NEW"
        if row["Change Type"] == "REMOVED":
            return "REMOVED"
        if pd.isna(row["Delta (Days)"]):
            return "UNKNOWN"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] < 0:
            return "AHEAD"
        return "UNCHANGED"

    df["Status"] = df.apply(status, axis=1)

    def comment(row):
        return {
            "DELAYED": "Shifted later, coordination required",
            "AHEAD": "Pulled earlier, potential float gain",
            "UNCHANGED": "Stable",
            "NEW": "Added scope in CL32",
            "REMOVED": "Dropped from CL32"
        }.get(row["Status"], "")

    df["Status / Comment"] = df.apply(comment, axis=1)

    return df[[
        "Activity",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Status",
        "Change Type",
        "Status / Comment"
    ]]