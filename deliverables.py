import pandas as pd


def build_deliverables(cl31, cl32):

    df = pd.merge(
        cl31,
        cl32,
        on="Activity Name",
        how="outer"
    )

    # Rename for clarity ONLY
    df.rename(columns={
        "BL Project Finish": "CL31 Finish",
        "Finish": "CL32 Finish"
    }, inplace=True)

    # =========================
    # FORMAT DATES
    # =========================
    def fmt(x):
        return "-" if pd.isna(x) else x.strftime("%d-%b-%y")

    df["CL31 Finish_fmt"] = df["CL31 Finish"].apply(fmt)
    df["CL32 Finish_fmt"] = df["CL32 Finish"].apply(fmt)

    # =========================
    # DELTA
    # =========================
    df["Delta (Days)"] = (
        df["CL32 Finish"] - df["CL31 Finish"]
    ).dt.days

    # =========================
    # CHANGE TYPE
    # =========================
    def classify(row):
        if pd.isna(row["CL31 Finish"]) and pd.notna(row["CL32 Finish"]):
            return "NEW"
        if pd.notna(row["CL31 Finish"]) and pd.isna(row["CL32 Finish"]):
            return "REMOVED"
        if pd.isna(row["Delta (Days)"]):
            return "UNCHANGED"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] < 0:
            return "EARLY"
        return "UNCHANGED"

    df["Change Type"] = df.apply(classify, axis=1)

    # =========================
    # FINAL OUTPUT (NO REORDERING, NO GROUPING LOGIC)
    # =========================
    out = df[[
        "Activity Name",
        "CL31 Finish_fmt",
        "CL32 Finish_fmt",
        "Delta (Days)",
        "Change Type"
    ]]

    out.rename(columns={
        "CL31 Finish_fmt": "CL31 Finish",
        "CL32 Finish_fmt": "CL32 Finish"
    }, inplace=True)

    return out