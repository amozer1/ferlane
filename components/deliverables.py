import pandas as pd

def build_design_control_table(cl31, cl32):

    # -------------------------
    # SAFE COLUMN CHECKS
    # -------------------------
    if "Discipline" not in cl31.columns:
        cl31["Discipline"] = "Unknown"

    # -------------------------
    # MERGE
    # -------------------------
    df = cl31.merge(
        cl32[["Activity ID", "CL32 Finish"]] if "CL32 Finish" in cl32.columns else cl32[["Activity ID"]],
        on="Activity ID",
        how="left"
    )

    # -------------------------
    # ENSURE CORE COLUMNS EXIST
    # -------------------------
    df["CL31 Finish"] = df["CL31 Finish"] if "CL31 Finish" in df.columns else pd.NaT
    df["CL32 Finish"] = df["CL32 Finish"] if "CL32 Finish" in df.columns else pd.NaT

    if "Activity Name_CL31" not in df.columns:
        df["Activity Name_CL31"] = df.get("Activity Name", "Unknown")

    if "Discipline" not in df.columns:
        df["Discipline"] = "Unknown"

    # -------------------------
    # VARIANCE
    # -------------------------
    df["Variance (days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

    # -------------------------
    # TREND
    # -------------------------
    def trend(r):
        if pd.isna(r["CL32 Finish"]):
            return "❓ Missing CL32"
        if r["Variance (days)"] > 0:
            return "🔺 Slipped"
        if r["Variance (days)"] < 0:
            return "🔻 Improved"
        return "➖ No Change"

    df["Trend"] = df.apply(trend, axis=1)

    # -------------------------
    # STATUS
    # -------------------------
    def status(r):
        if pd.isna(r["CL32 Finish"]):
            return "🟡 No Update"

        v = r["Variance (days)"]

        if v >= 7:
            return "🔴 Critical Delay"
        if v >= 3:
            return "🟠 At Risk"
        if v > -3:
            return "🟡 Monitor"
        return "🟢 Ahead"

    df["Status"] = df.apply(status, axis=1)

    # -------------------------
    # FLOAT
    # -------------------------
    df["Float"] = ""

    # -------------------------
    # FINAL SAFE OUTPUT
    # -------------------------
    return df[[
        "Activity ID",
        "Activity Name_CL31",
        "Discipline",
        "CL31 Finish",
        "CL32 Finish",
        "Variance (days)",
        "Trend",
        "Float",
        "Status"
    ]]