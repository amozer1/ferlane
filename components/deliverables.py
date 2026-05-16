import pandas as pd

def build_deliverables(df31: pd.DataFrame, df32: pd.DataFrame) -> pd.DataFrame:
    """
    Compare CL31 vs CL32 and generate deliverables delta table
    """

    def is_deliverable(name):
        if pd.isna(name):
            return False
        name = str(name).lower()
        keywords = ["design", "submission", "pack", "drawing", "deliverable", "assessment"]
        return any(k in name for k in keywords)

    # Filter deliverables
    d31 = df31[df31["Activity Name"].apply(is_deliverable)].copy()
    d32 = df32[df32["Activity Name"].apply(is_deliverable)].copy()

    # Standardise
    d31 = d31.rename(columns={"Finish": "CL31 Finish"})
    d32 = d32.rename(columns={"Finish": "CL32 Finish"})

    d31 = d31[["Activity Name", "CL31 Finish"]]
    d32 = d32[["Activity Name", "CL32 Finish"]]

    # Merge
    merged = pd.merge(d31, d32, on="Activity Name", how="outer")

    # Delta calculation
    merged["Delta (Days)"] = (
        pd.to_datetime(merged["CL32 Finish"], errors="coerce")
        - pd.to_datetime(merged["CL31 Finish"], errors="coerce")
    ).dt.days

    # Classification (FIXED SYNTAX)
    def classify(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"

        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"

        if pd.isna(row["Delta (Days)"]):
            return "UNKNOWN"

        if row["Delta (Days)"] == 0:
            return "UNCHANGED"

        if row["Delta (Days)"] > 0:
            return "DELAYED"

        return "ACCELERATED"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # Comments
    def comment(row):
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "ACCELERATED":
            return "Pulled earlier, improved sequencing"
        if row["Change Type"] == "NEW":
            return "Added scope in CL32"
        if row["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        return "Stable"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    return merged