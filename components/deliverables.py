import pandas as pd
import numpy as np


# ----------------------------
# 1. Identify valid deliverables
# ----------------------------
def is_deliverable(activity_name: str) -> bool:
    """
    Rules to decide if row is a deliverable.
    """

    if pd.isna(activity_name):
        return False

    name = str(activity_name).strip()

    if name == "":
        return False

    # Exclusions
    exclude_keywords = [
        "[GET]",
        "Mobilisation",
        "Review Information",
        "Meeting",
        "Response",
        "Key Dates",
        "Contract",
        "Site Visit",
        "Model",
        "Build Terrain",
        "BIM Set Up"
    ]

    for kw in exclude_keywords:
        if kw.lower() in name.lower():
            return False

    # Must contain meaningful output indicator
    output_keywords = [
        "Design",
        "Drawing",
        "Model",
        "Assessment",
        "Report",
        "Schedule",
        "Specification",
        "Calculation",
        "Pack",
        "Plan",
        "Details",
        "Layout",
        "GA",
        "Concept",
        "Design Pack"
    ]

    return any(k.lower() in name.lower() for k in output_keywords)


# ----------------------------
# 2. Extract deliverables only
# ----------------------------
def extract_deliverables(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df = df[df["Activity Name"].apply(is_deliverable)]

    return df


# ----------------------------
# 3. Build CL31 vs CL32 comparison
# ----------------------------
def build_comparison(cl31: pd.DataFrame, cl32: pd.DataFrame) -> pd.DataFrame:

    # Standardise keys
    cl31 = cl31.copy()
    cl32 = cl32.copy()

    cl31["Activity Name"] = cl31["Activity Name"].astype(str).str.strip()
    cl32["Activity Name"] = cl32["Activity Name"].astype(str).str.strip()

    # Extract deliverables
    d31 = extract_deliverables(cl31)
    d32 = extract_deliverables(cl32)

    # Merge
    merged = pd.merge(
        d31,
        d32,
        on="Activity Name",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # Dates
    merged["CL31 Finish"] = merged.get("Finish_CL31")
    merged["CL32 Finish"] = merged.get("Finish_CL32")

    # Delta calculation
    merged["Delta (Days)"] = (
        (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days
    )

    # Change Type
    def classify(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        elif pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        elif pd.isna(row["Delta (Days)"]):
            return "UNKNOWN"
        elif row["Delta (Days)"] > 0:
            return "DELAYED"
        elif row["Delta (Days)"] < 0:
            return "ACCELERATED"
        else:
            return "UNCHANGED"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # Status
    def status(row):
        if row["Change Type"] == "DELAYED":
            return "⚠️ Slipped"
        elif row["Change Type"] == "ACCELERATED":
            return "🟢 Improved"
        elif row["Change Type"] == "NEW":
            return "🆕 Added"
        elif row["Change Type"] == "REMOVED":
            return "❌ Removed"
        else:
            return "🟡 Stable"

    merged["Status / Comment"] = merged.apply(status, axis=1)

    # Final structure
    final = merged[[
        "Activity Name",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return final.sort_values(by="Change Type")