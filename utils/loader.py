import pandas as pd


def clean_dates(df):
    """Remove A / * from dates and standardise."""
    for col in df.columns:
        if "Start" in col or "Finish" in col:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(" A", "", regex=False)
                .str.replace("*", "", regex=False)
            )
    return df


def prepare_dataframe(file):
    df = pd.read_excel(file)
    df = clean_dates(df)

    # Keep only deliverable-level rows (avoid group headers)
    df = df[df["Activity Name"].notna()].copy()

    # Normalize key
    df["Deliverable"] = df["Activity Name"].astype(str).str.strip()

    return df


def build_lookup(df, finish_col="Finish"):
    """
    IMPORTANT FIX:
    Handle duplicate deliverables safely by taking MAX date (latest finish)
    """
    df[finish_col] = pd.to_datetime(df[finish_col], errors="coerce")

    lookup = (
        df.groupby("Deliverable")[finish_col]
        .max()
    )

    return lookup


def prepare_comparison_df(df31, df32):
    df31 = prepare_dataframe(df31)
    df32 = prepare_dataframe(df32)

    # unified deliverables
    all_deliverables = sorted(
        set(df31["Deliverable"]).union(set(df32["Deliverable"]))
    )

    merged = pd.DataFrame({"Deliverable": all_deliverables})

    # SAFE LOOKUPS (no map error)
    df31_lookup = build_lookup(df31)
    df32_lookup = build_lookup(df32)

    merged["CL31 Finish"] = merged["Deliverable"].map(df31_lookup)
    merged["CL32 Finish"] = merged["Deliverable"].map(df32_lookup)

    # Delta
    merged["Delta (Days)"] = (
        (merged["CL32 Finish"] - merged["CL31 Finish"])
        .dt.days
    )

    return merged