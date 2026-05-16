import pandas as pd
import numpy as np

def build_deliverables_report(cl31, cl32):

    df = pd.merge(
        cl31[["Activity", "CL31 Finish"]],
        cl32[["Activity", "CL32 Finish"]],
        on="Activity",
        how="outer"
    )

    # -----------------------------
    # CHANGE TYPE
    # -----------------------------
    def change_type(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        return "COMPARE"

    df["Change Type"] = df.apply(change_type, axis=1)

    # -----------------------------
    # DELTA
    # -----------------------------
    def delta_days(row):
        if row["Change Type"] != "COMPARE":
            return np.nan
        return (row["CL32 Finish"] - row["CL31 Finish"]).days

    df["Delta (Days)"] = df.apply(delta_days, axis=1)

    # -----------------------------
    # STATUS
    # -----------------------------
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

    # -----------------------------
    # COMMENT
    # -----------------------------
    def comment(row):
        if row["Status"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Status"] == "AHEAD":
            return "Pulled earlier, potential float gain"
        if row["Status"] == "UNCHANGED":
            return "Stable"
        if row["Status"] == "NEW":
            return "Added scope in CL32"
        if row["Status"] == "REMOVED":
            return "Dropped from CL32"
        return ""

    df["Status / Comment"] = df.apply(comment, axis=1)

    # Clean ordering
    df = df[[
        "Activity",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Status",
        "Change Type",
        "Status / Comment"
    ]]

    return df