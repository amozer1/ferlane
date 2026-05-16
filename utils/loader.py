import pandas as pd


CL31_PATH = "data/CL31-February.xlsx"
CL32_PATH = "data/CL32-May.xlsx"


def load_programme(path: str) -> pd.DataFrame:
    """
    Strict auto-load from repo only.
    """
    df = pd.read_excel(path, engine="openpyxl")
    df.columns = df.columns.str.strip()
    return df


def prepare_comparison_df():

    df31 = load_programme(CL31_PATH)
    df32 = load_programme(CL32_PATH)

    # Standardise structure
    df31 = df31[["Activity Name", "Finish"]].copy()
    df32 = df32[["Activity Name", "Finish"]].copy()

    df31.columns = ["Deliverable", "CL31 Finish"]
    df32.columns = ["Deliverable", "CL32 Finish"]

    # Convert dates
    df31["CL31 Finish"] = pd.to_datetime(df31["CL31 Finish"], errors="coerce")
    df32["CL32 Finish"] = pd.to_datetime(df32["CL32 Finish"], errors="coerce")

    # Merge ALL deliverables (CL32 drives structure)
    df = pd.merge(df31, df32, on="Deliverable", how="outer")

    # Delta
    df["Delta (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

    # Classification
    def classify(r):
        if pd.isna(r["CL31 Finish"]) and pd.notna(r["CL32 Finish"]):
            return "NEW"
        if pd.isna(r["CL32 Finish"]) and pd.notna(r["CL31 Finish"]):
            return "REMOVED"
        if pd.isna(r["Delta (Days)"]):
            return "UNKNOWN"
        if r["Delta (Days)"] < 0:
            return "ACCELERATED"
        if r["Delta (Days)"] > 0:
            return "DELAYED"
        return "UNCHANGED"

    df["Change Type"] = df.apply(classify, axis=1)

    return df