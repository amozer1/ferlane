import pandas as pd


def clean(df):
    df = df.copy()

    # remove summary/header rows
    df = df[df["Activity ID"].astype(str).str.contains("FER-", na=False)]

    df = df[df["Activity Name"].notna()].copy()

    df["Deliverable"] = df["Activity Name"].astype(str).str.strip()

    # clean date noise (A, *)
    for col in ["Finish"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(" A", "", regex=False)
                .str.replace("*", "", regex=False)
            )

    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    return df


def build_lookup(df):
    return df.groupby("Deliverable")["Finish"].max()


def prepare_comparison_df(df31, df32):

    df31 = clean(df31)
    df32 = clean(df32)

    cl31 = build_lookup(df31)
    cl32 = build_lookup(df32)

    all_deliverables = sorted(set(cl31.index).union(set(cl32.index)))

    merged = pd.DataFrame({"Deliverable": all_deliverables})

    merged["CL31 Finish"] = merged["Deliverable"].map(cl31)
    merged["CL32 Finish"] = merged["Deliverable"].map(cl32)

    # keep only rows where at least one exists
    merged = merged[
        merged["CL31 Finish"].notna() |
        merged["CL32 Finish"].notna()
    ].copy()

    # Delta
    merged["Delta (Days)"] = (
        merged["CL32 Finish"] - merged["CL31 Finish"]
    ).dt.days

    # Change Type
    def change_type(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        if pd.isna(row["Delta (Days)"]):
            return "NEW"
        if row["Delta (Days)"] == 0:
            return "UNCHANGED"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        return "ACCELERATED"

    merged["Change Type"] = merged.apply(change_type, axis=1)

    return merged