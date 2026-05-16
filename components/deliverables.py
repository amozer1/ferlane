import pandas as pd


def _clean(df):
    df = df.copy()

    # Ensure required column exists
    if "Activity Name" not in df.columns:
        return pd.DataFrame(columns=["Activity Name", "Finish"])

    df = df[["Activity Name", "Finish"]].dropna(subset=["Activity Name"])

    # remove hierarchy rows (summary headings)
    df = df[~df["Activity Name"].str.contains("Programme|Design|Package|Key Dates|Milestones|Deliverables|Construction|Retired", na=False)]

    return df


def build_deliverables_card(cl31_df, cl32_df):

    cl31 = _clean(cl31_df)
    cl32 = _clean(cl32_df)

    # Merge on Activity Name
    merged = pd.merge(
        cl31,
        cl32,
        on="Activity Name",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # Convert dates safely
    for col in ["Finish_CL31", "Finish_CL32"]:
        merged[col] = pd.to_datetime(merged[col], errors="coerce")

    # Calculate delta
    merged["Δ Finish (Days)"] = (
        merged["Finish_CL32"] - merged["Finish_CL31"]
    ).dt.days

    # Float change (simple proxy if not explicitly provided)
    merged["Float Change"] = merged["Δ Finish (Days)"].fillna(0) * -1

    # Status logic
    def status(x):
        if pd.isna(x):
            return "⚪ Missing"
        if x > 10:
            return "🔴 Delayed"
        if x > 0:
            return "🟡 At Risk"
        return "🟢 On Track"

    merged["Status"] = merged["Δ Finish (Days)"].apply(status)

    # Final format
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