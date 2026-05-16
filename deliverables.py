import pandas as pd


def _clean_date(series: pd.Series) -> pd.Series:
    series = series.astype(str).str.replace("A", "", regex=False).str.strip()
    series = series.replace(["", "nan", "None"], pd.NA)
    return pd.to_datetime(series, errors="coerce", dayfirst=True)


def build_deliverables(df31, df32):

    # =========================
    # CL31 (BASELINE)
    # =========================
    cl31 = df31.copy()
    cl31["Deliverable"] = cl31["Activity Name"].astype(str).str.strip()
    cl31["CL31 Finish"] = _clean_date(cl31["BL Project Finish"])
    cl31 = cl31[["Deliverable", "CL31 Finish"]]

    # =========================
    # CL32 (CURRENT PROGRAMME)
    # =========================
    cl32 = df32.copy()
    cl32["Deliverable"] = cl32["Activity Name"].astype(str).str.strip()
    cl32["CL32 Finish"] = _clean_date(cl32["Finish"])
    cl32 = cl32[["Deliverable", "CL32 Finish"]]

    # =========================
    # MERGE
    # =========================
    merged = pd.merge(cl31, cl32, on="Deliverable", how="outer")

    # =========================
    # DELTA
    # =========================
    merged["Delta (Days)"] = (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days

    # =========================
    # CHANGE TYPE
    # =========================
    def classify(row):
        if pd.isna(row["CL31 Finish"]) and not pd.isna(row["CL32 Finish"]):
            return "NEW"

        if not pd.isna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"

        if pd.isna(row["Delta (Days)"]):
            return "UNCHANGED"

        if row["Delta (Days)"] > 0:
            return "DELAYED"

        if row["Delta (Days)"] < 0:
            return "EARLY"

        return "UNCHANGED"

    merged["Change Type"] = merged.apply(classify, axis=1)

    # =========================
    # COMMENTS
    # =========================
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

    # =========================
    # FORMAT DATES
    # =========================
    merged["CL31 Finish"] = merged["CL31 Finish"].dt.strftime("%d-%b-%y").fillna("-")
    merged["CL32 Finish"] = merged["CL32 Finish"].dt.strftime("%d-%b-%y").fillna("-")

    # =========================
    # FINAL OUTPUT
    # =========================
    result = merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    return result.sort_values(by="Change Type")