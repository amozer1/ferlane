import pandas as pd


def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip()
    return df


def load_programme(uploaded_file: str | object) -> pd.DataFrame:
    """
    Loads programme data from uploaded Excel file or file path.
    """
    if uploaded_file is None:
        return pd.DataFrame()

    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        df = _clean_columns(df)
        return df
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")


def prepare_comparison_df(file31, file32) -> pd.DataFrame:
    """
    Creates CL31 vs CL32 comparison dataset dynamically.
    """

    df31 = load_programme(file31)
    df32 = load_programme(file32)

    if df31.empty or df32.empty:
        return pd.DataFrame()

    # Standardise column names
    def standardise(df):
        # Try flexible column detection
        deliverable_col = "Activity Name" if "Activity Name" in df.columns else None
        finish_col = "Finish" if "Finish" in df.columns else None

        if not deliverable_col or not finish_col:
            raise ValueError("Missing required columns: 'Activity Name' or 'Finish'")

        df = df[[deliverable_col, finish_col]].copy()
        df.columns = ["Deliverable", "Finish"]
        return df

    df31 = standardise(df31)
    df32 = standardise(df32)

    # Convert dates safely
    df31["Finish"] = pd.to_datetime(df31["Finish"], errors="coerce")
    df32["Finish"] = pd.to_datetime(df32["Finish"], errors="coerce")

    df31 = df31.rename(columns={"Finish": "CL31 Finish"})
    df32 = df32.rename(columns={"Finish": "CL32 Finish"})

    # Merge EVERYTHING (treat all CL32 as deliverables baseline)
    df = pd.merge(df31, df32, on="Deliverable", how="outer")

    # Delta calculation
    df["Delta (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

    # Change classification
    def classify(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"

        if pd.isna(row["CL32 Finish"]) and pd.notna(row["CL31 Finish"]):
            return "REMOVED"

        if pd.isna(row["Delta (Days)"]):
            return "UNKNOWN"

        if row["Delta (Days)"] < 0:
            return "ACCELERATED"

        if row["Delta (Days)"] > 0:
            return "DELAYED"

        return "UNCHANGED"

    df["Change Type"] = df.apply(classify, axis=1)

    # Status messages
    status_map = {
        "ACCELERATED": "Earlier than CL31 baseline",
        "DELAYED": "Shifted later, coordination required",
        "NEW": "Added in CL32",
        "REMOVED": "Dropped from CL32",
        "UNCHANGED": "No change",
        "UNKNOWN": "Insufficient data"
    }

    df["Status / Comment"] = df["Change Type"].map(status_map)

    # Sort for readability
    df = df.sort_values(by=["Change Type", "Deliverable"], na_position="last")

    return df