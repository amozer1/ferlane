import pandas as pd


def clean_dates(df):
    for col in df.columns:
        if "Start" in col or "Finish" in col:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(" A", "", regex=False)
                .str.replace("*", "", regex=False)
            )
    return df


def prepare_dataframe(df):
    """
    FIX: Now expects a DataFrame, NOT a file path
    """
    if isinstance(df, str):
        df = pd.read_excel(df)
    elif hasattr(df, "read"):
        # uploaded file from Streamlit
        df = pd.read_excel(df)

    df = clean_dates(df)

    df = df[df["Activity Name"].notna()].copy()
    df["Deliverable"] = df["Activity Name"].astype(str).str.strip()

    return df


def build_lookup(df, col="Finish"):
    df[col] = pd.to_datetime(df[col], errors="coerce")

    return df.groupby("Deliverable")[col].max()


def prepare_comparison_df(df31, df32):

    df31 = prepare_dataframe(df31)
    df32 = prepare_dataframe(df32)

    all_deliverables = sorted(
        set(df31["Deliverable"]).union(set(df32["Deliverable"]))
    )

    merged = pd.DataFrame({"Deliverable": all_deliverables})

    df31_map = build_lookup(df31)
    df32_map = build_lookup(df32)

    merged["CL31 Finish"] = merged["Deliverable"].map(df31_map)
    merged["CL32 Finish"] = merged["Deliverable"].map(df32_map)

    merged["Delta (Days)"] = (
        (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days
    )

    return merged