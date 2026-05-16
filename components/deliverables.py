import pandas as pd
from utils.loader import is_deliverable_row, clean_date


def build_deliverable_comparison(df31, df32):

    # -------------------------
    # STEP 1: LOCI FILTERING
    # -------------------------
    df31 = df31[df31.apply(is_deliverable_row, axis=1)].copy()
    df32 = df32[df32.apply(is_deliverable_row, axis=1)].copy()

    # -------------------------
    # STEP 2: KEEP ORIGINAL NAME (NO TRANSFORM)
    # -------------------------
    df31["Deliverable"] = df31["Activity Name"]
    df32["Deliverable"] = df32["Activity Name"]

    # -------------------------
    # STEP 3: CLEAN DATES ONLY
    # -------------------------
    df31["CL31 Finish"] = df31["Finish"].apply(clean_date)
    df32["CL32 Finish"] = df32["Finish"].apply(clean_date)

    # -------------------------
    # STEP 4: MERGE
    # -------------------------
    merged = pd.merge(
        df31[["Deliverable", "CL31 Finish"]],
        df32[["Deliverable", "CL32 Finish"]],
        on="Deliverable",
        how="outer"
    )

    # -------------------------
    # STEP 5: DELTA
    # -------------------------
    merged["Delta (Days)"] = (
        merged["CL32 Finish"] - merged["CL31 Finish"]
    ).dt.days

    # -------------------------
    # STEP 6: CHANGE TYPE
    # -------------------------
    def change_type(r):
        if pd.isna(r["CL31 Finish"]) and pd.notna(r["CL32 Finish"]):
            return "NEW"
        if pd.notna(r["CL31 Finish"]) and pd.isna(r["CL32 Finish"]):
            return "REMOVED"
        if pd.notna(r["Delta (Days)"]) and r["Delta (Days)"] > 0:
            return "DELAYED"
        if pd.notna(r["Delta (Days)"]) and r["Delta (Days)"] < 0:
            return "ACCELERATED"
        return "UNCHANGED"

    merged["Change Type"] = merged.apply(change_type, axis=1)

    # -------------------------
    # STEP 7: OUTPUT FORMAT ONLY
    # -------------------------
    merged["CL31 Finish"] = pd.to_datetime(merged["CL31 Finish"]).dt.strftime("%d-%b-%Y")
    merged["CL32 Finish"] = pd.to_datetime(merged["CL32 Finish"]).dt.strftime("%d-%b-%Y")

    merged["Delta (Days)"] = merged["Delta (Days)"].fillna("—")

    merged["Status / Comment"] = merged["Change Type"].map({
        "DELAYED": "Shifted later, coordination required",
        "ACCELERATED": "Moved earlier",
        "NEW": "Added in CL32",
        "REMOVED": "Dropped from CL32",
        "UNCHANGED": "Stable"
    })

    return merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]