import pandas as pd

def build_deliverables(df31: pd.DataFrame, df32: pd.DataFrame) -> pd.DataFrame:
    """
    Compare CL31 vs CL32 and generate deliverable delta table
    """

    def is_deliverable(name):
        if pd.isna(name):
            return False
        name = str(name).lower()
        return any(x in name for x in ["design", "submission", "pack", "drawing", "deliverable"])

    df31d = df31[df31["Activity Name"].apply(is_deliverable)].copy()
    df32d = df32[df32["Activity Name"].apply(is_deliverable)].copy()

    df31d = df31d.rename(columns={"Finish": "CL31 Finish"})
    df32d = df32d.rename(columns={"Finish": "CL32 Finish"})

    df31d = df31d[["Activity Name", "CL31 Finish"]]
    df32d = df32d[["Activity Name", "CL32 Finish"]]

    merged = pd.merge(df31d, df32d, on="Activity Name", how="outer")

    merged["Delta (Days)"] = (
        pd.to_datetime(merged["CL32 Finish"], errors="coerce")
        - pd.to_datetime(merged["CL31 Finish"], errors="coerce")
    ).dt.days

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