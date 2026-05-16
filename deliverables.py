import pandas as pd


def _prepare(df, finish_col):
    df = df.copy()

    df = df[["Activity", finish_col]].dropna(subset=["Activity"])

    df = df.rename(columns={finish_col: "Finish"})
    df["Activity"] = df["Activity"].astype(str).str.strip()

    return df


def build_deliverables(df31, df32):

    df31 = _prepare(df31, "Finish")
    df32 = _prepare(df32, "Finish")

    merged = pd.merge(
        df31,
        df32,
        on="Activity",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # ensure datetime
    merged["Finish_CL31"] = pd.to_datetime(merged["Finish_CL31"], errors="coerce")
    merged["Finish_CL32"] = pd.to_datetime(merged["Finish_CL32"], errors="coerce")

    # delta days
    merged["Delta (Days)"] = (merged["Finish_CL32"] - merged["Finish_CL31"]).dt.days

    # change type
    def classify(row):
        if pd.isna(row["Finish_CL31"]) and not pd.isna(row["Finish_CL32"]):
            return "NEW"
        elif not pd.isna(row["Finish_CL31"]) and pd.isna(row["Finish_CL32"]):
            return "REMOVED"
        elif pd.isna(row["Delta (Days)"]):
            return "UNCHANGED"
        elif row["Delta (Days)"] > 0:
            return "DELAYED"
        elif row["Delta (Days)"] < 0:
            return "EARLY"
        else:
            return "UNCHANGED"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # float placeholder (you can map later properly)
    merged["Float"] = ""

    # status comment
    def comment(row):
        if row["Change Type"] == "NEW":
            return "Added scope in CL32"
        if row["Change Type"] == "REMOVED":
            return "Removed from CL32"
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "EARLY":
            return "Pulled forward"
        return "Stable"

    merged["Status / Comment"] = merged.apply(comment, axis=1)

    # format dates (IMPORTANT FIX YOU ASKED)
    merged["CL31 Finish"] = merged["Finish_CL31"].dt.strftime("%d-%b-%y").fillna("-")
    merged["CL32 Finish"] = merged["Finish_CL32"].dt.strftime("%d-%b-%y").fillna("-")

    result = merged[[
        "Activity",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Float",
        "Change Type",
        "Status / Comment"
    ]].rename(columns={"Activity": "Deliverable"})

    return result.sort_values(by="Change Type")