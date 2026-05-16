import pandas as pd
import numpy as np

def build_deliverables_report(cl31, cl32):

    df = pd.merge(cl31, cl32, on="Deliverable", how="outer")

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
    def delta(row):
        if row["Change Type"] != "COMPARE":
            return None
        return (row["CL32 Finish"] - row["CL31 Finish"]).days

    df["Delta (Days)"] = df.apply(delta, axis=1)

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
    # COMMENT ENGINE
    # -----------------------------
    def comment(row):
        return {
            "DELAYED": "Shifted later, coordination required",
            "AHEAD": "Pulled earlier, programme gain",
            "UNCHANGED": "Stable",
            "NEW": "Added scope in CL32",
            "REMOVED": "Dropped from CL32"
        }.get(row["Status"], "")

    df["Comment"] = df.apply(comment, axis=1)

    # FORMAT DATES (IMPORTANT REQUEST YOU MADE)
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"]).dt.strftime("%d-%b-%Y")
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"]).dt.strftime("%d-%b-%Y")

    return df[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Status",
        "Comment"
    ]]