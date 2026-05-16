import pandas as pd


def _normalize_columns(df):
    df = df.copy()
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ")
    )
    return df


def _clean(df):
    df = _normalize_columns(df)

    if "Activity Name" not in df.columns:
        return pd.DataFrame()

    df = df[df["Activity Name"].notna()].copy()
    return df


def _find_finish_column(df, candidates):
    """
    Finds first matching column from list of possible names
    """
    for c in candidates:
        if c in df.columns:
            return pd.to_datetime(df[c], errors="coerce")
    return pd.Series([pd.NaT] * len(df))


def build_deliverables_card(cl31_df, cl32_df):

    cl31 = _clean(cl31_df)
    cl32 = _clean(cl32_df)

    # -----------------------------
    # SAFE COLUMN DETECTION
    # -----------------------------
    cl31["CL31 Finish"] = _find_finish_column(
        cl31,
        ["BL Project Finish", "Finish", "BL Finish", "Baseline Finish"]
    )

    cl32["CL32 Finish"] = _find_finish_column(
        cl32,
        ["BL1 Finish", "BL Finish", "Finish", "Baseline Finish"]
    )

    # -----------------------------
    # MERGE
    # -----------------------------
    merged = pd.merge(
        cl31[["Activity Name", "CL31 Finish"]],
        cl32[["Activity Name", "CL32 Finish"]],
        on="Activity Name",
        how="outer"
    )

    # -----------------------------
    # DELTA
    # -----------------------------
    merged["Δ Finish (Days)"] = (
        merged["CL32 Finish"] - merged["CL31 Finish"]
    ).dt.days

    merged["Float Change"] = merged["Δ Finish (Days)"].fillna(0) * -1

    # -----------------------------
    # STATUS
    # -----------------------------
    def status(x):
        if pd.isna(x):
            return "⚪ Missing"
        if x > 10:
            return "🔴 Delayed"
        if x > 0:
            return "🟡 At Risk"
        return "🟢 On Track"

    merged["Status"] = merged["Δ Finish (Days)"].apply(status)

    # -----------------------------
    # FINAL OUTPUT
    # -----------------------------
    final = merged[
        [
            "Activity Name",
            "CL31 Finish",
            "CL32 Finish",
            "Δ Finish (Days)",
            "Float Change",
            "Status"
        ]
    ]

    return final.sort_values("Δ Finish (Days)", na_position="last")