import pandas as pd


def _clean(df):
    df = df.copy()
    df.columns = df.columns.str.strip()

    if "Activity Name" not in df.columns:
        return pd.DataFrame()

    df = df[df["Activity Name"].notna()].copy()
    return df


def _get_finish(df, primary, fallback="Finish"):
    if primary in df.columns:
        return pd.to_datetime(df[primary], errors="coerce")
    if fallback in df.columns:
        return pd.to_datetime(df[fallback], errors="coerce")
    return pd.Series([pd.NaT] * len(df))


def build_deliverables_card(cl31_df, cl32_df):

    cl31 = _clean(cl31_df)
    cl32 = _clean(cl32_df)

    # -----------------------------
    # STANDARDISE FINISH FIELDS
    # -----------------------------
    cl31["CL31 Finish"] = _get_finish(cl31, "BL Project Finish")
    cl32["CL32 Finish"] = _get_finish(cl32, "BL1 Finish")

    # -----------------------------
    # MERGE ONLY WHAT WE NEED
    # -----------------------------
    merged = pd.merge(
        cl31[["Activity Name", "CL31 Finish"]],
        cl32[["Activity Name", "CL32 Finish"]],
        on="Activity Name",
        how="outer"
    )

    # -----------------------------
    # DELTA CALCULATION
    # -----------------------------
    merged["Δ Finish (Days)"] = (
        merged["CL32 Finish"] - merged["CL31 Finish"]
    ).dt.days

    merged["Float Change"] = merged["Δ Finish (Days)"].fillna(0) * -1

    # -----------------------------
    # STATUS LOGIC
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
    # FINAL OUTPUT CARD
    # -----------------------------
    final = merged[[
        "Activity Name",
        "CL31 Finish",
        "CL32 Finish",
        "Δ Finish (Days)",
        "Float Change",
        "Status"
    ]]

    return final.sort_values("Δ Finish (Days)", na_position="last")