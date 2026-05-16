import pandas as pd


def build_deliverables(cl31, cl32):

    # =========================
    # STANDARDISE KEYS
    # =========================
    cl31 = cl31.copy()
    cl32 = cl32.copy()

    cl31["Deliverable"] = cl31["Activity Name"].astype(str).str.strip()
    cl32["Deliverable"] = cl32["Activity Name"].astype(str).str.strip()

    # =========================
    # KEEP ONLY NEEDED FIELDS
    # =========================
    cl31 = cl31[["Deliverable", "BL Project Finish"]]
    cl32 = cl32[["Deliverable", "Finish"]]

    # =========================
    # MERGE
    # =========================
    df = pd.merge(
        cl31,
        cl32,
        on="Deliverable",
        how="outer"
    )

    # =========================
    # RENAME FOR CLARITY
    # =========================
    df.rename(columns={
        "BL Project Finish": "CL31 Finish",
        "Finish": "CL32 Finish"
    }, inplace=True)

    # =========================
    # FORMAT DATES
    # =========================
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"], errors="coerce")
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"], errors="coerce")

    # =========================
    # DATE FORMATTING
    # =========================
    def fmt(x):
        return "-" if pd.isna(x) else x.strftime("%d-%b-%y")

    df["CL31 Finish_fmt"] = df["CL31 Finish"].apply(fmt)
    df["CL32 Finish_fmt"] = df["CL32 Finish"].apply(fmt)

    # =========================
    # DELTA
    # =========================
    df["Delta (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

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
    # STATUS COMMENT
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

    df["Status / Comment"] = df.apply(comment, axis=1)

    # =========================
    # FINAL OUTPUT
    # =========================
    out = df[[
        "Deliverable",
        "CL31 Finish_fmt",
        "CL32 Finish_fmt",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]]

    out.rename(columns={
        "CL31 Finish_fmt": "CL31 Finish",
        "CL32 Finish_fmt": "CL32 Finish"
    }, inplace=True)

    return out.sort_values("Deliverable")