import pandas as pd
import numpy as np


# ---------- NORMALISE ----------
def _extract(df, cl_label):
    df = df.copy()

    df = df.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": f"{cl_label} Finish"
    })

    return df[["Deliverable", f"{cl_label} Finish"]]


# ---------- DELTA SAFE CALC ----------
def safe_delta(cl31, cl32):
    if pd.isna(cl31) or pd.isna(cl32):
        return np.nan
    return (cl32 - cl31).days


# ---------- CLASSIFICATION ----------
def classify(row):
    if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
        return "NEW"

    if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
        return "REMOVED"

    if pd.isna(row["Delta (Days)"]):
        return "UNKNOWN"

    if row["Delta (Days)"] == 0:
        return "UNCHANGED"

    return "DELAYED" if row["Delta (Days)"] > 0 else "EARLY"


# ---------- COMMENT ENGINE ----------
def comment(row):
    if row["Change Type"] == "NEW":
        return "Added scope in CL32"

    if row["Change Type"] == "REMOVED":
        return "Dropped from CL32"

    if row["Change Type"] == "UNCHANGED":
        return "Stable"

    if row["Change Type"] == "DELAYED":
        if row["Delta (Days)"] <= 14:
            return "Minor slip, gateway impact"
        return "Shifted later, coordination required"

    if row["Change Type"] == "EARLY":
        return "Pulled earlier than baseline"

    return "Review required"


# ---------- MAIN BUILDER ----------
def build_deliverables(df31, df32):

    df31 = _extract(df31, "CL31")
    df32 = _extract(df32, "CL32")

    df = pd.merge(df31, df32, on="Deliverable", how="outer")

    # ensure datetime
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"], errors="coerce")
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"], errors="coerce")

    # delta
    df["Delta (Days)"] = df.apply(
        lambda r: safe_delta(r["CL31 Finish"], r["CL32 Finish"]),
        axis=1
    )

    # type
    df["Change Type"] = df.apply(classify, axis=1)

    # comment
    df["Status / Comment"] = df.apply(comment, axis=1)

    # format output (final UI clean format)
    def fmt(x):
        return "—" if pd.isna(x) else x.strftime("%d-%b-%y")

    df["CL31 Finish"] = df["CL31 Finish"].apply(fmt)
    df["CL32 Finish"] = df["CL32 Finish"].apply(fmt)

    df["Delta (Days)"] = df["Delta (Days)"].apply(
        lambda x: "—" if pd.isna(x) else int(x)
    )

    return df[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]].sort_values("Change Type")