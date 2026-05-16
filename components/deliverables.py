import pandas as pd


def _get_col(df, preferred, fallback=None):
    """Safely get column that may or may not exist"""
    if preferred in df.columns:
        return df[preferred]
    if fallback and fallback in df.columns:
        return df[fallback]
    return pd.Series([pd.NaT] * len(df))


def _clean(df):
    df = df.copy()

    # strip column spaces (VERY IMPORTANT in Excel files)
    df.columns = df.columns.str.strip()

    if "Activity Name" not in df.columns:
        return pd.DataFrame()

    df = df[df["Activity Name"].notna()]

    return df


def build_deliverables_card(cl31_df, cl32_df):

    cl31 = _clean(cl31_df)
    cl32 = _clean(cl32_df)

    # -----------------------------
    # SAFE FINISH COLUMN HANDLING
    # -----------------------------
    cl31["Finish"] = _get_col(cl31, "BL1 Finish", "Finish")
    cl32["Finish"] = _get_col(cl32, "BL1 Finish", "Finish")

    # Convert dates safely
    cl31["Finish"] = pd.to_datetime(cl31["Finish"], errors="coerce")
    cl32["Finish"] = pd.to_datetime(cl32["Finish"], errors="coerce")

    # -----------------------------
    # MERGE
    # -----------------------------
    merged = pd.merge(
        cl31[["Activity Name", "Finish"]],
        cl32[["Activity Name", "Finish"]],
        on="Activity Name",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # -----------------------------
    # DELTA CALC
    # -----------------------------
    merged["Δ Finish (Days)"] = (
        merged["Finish_CL32"] - merged["Finish_CL31"]
    ).dt.days

    merged["Float Change"] = merged["Δ Finish (Days)"].fillna(0) * -1

    # -----------------------------
    # STATUS RULES
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
    final = merged[[
        "Activity Name",
        "Finish_CL31",
        "Finish_CL32",
        "Δ Finish (Days)",
        "Float Change",
        "Status"
    ]]

    final = final.rename(columns={
        "Finish_CL31": "CL31 Finish",
        "Finish_CL32": "CL32 Finish"
    })

    return final.sort_values("Δ Finish (Days)", na_position="last")