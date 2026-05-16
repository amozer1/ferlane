# components/deliverables.py
import pandas as pd

def build_design_control_table(cl31, cl32):

    # -------------------------
    # MERGE (THIS FIXES YOUR ISSUE)
    # -------------------------
    df = cl31.merge(
        cl32[["Activity ID", "CL32 Finish"]],
        on="Activity ID",
        how="left"
    )

    # -------------------------
    # RENAME SAFE FIELDS
    # -------------------------
    if "Activity Name_CL31" not in df.columns:
        df["Activity Name_CL31"] = df.get("Activity Name", "")

    # -------------------------
    # VARIANCE CALCULATION
    # -------------------------
    df["Variance (days)"] = (
        df["CL32 Finish"] - df["CL31 Finish"]
    ).dt.days

    # -------------------------
    # TREND LOGIC
    # -------------------------
    def trend(row):
        if pd.isna(row["CL32 Finish"]):
            return "❓ Missing CL32"
        if row["Variance (days)"] > 0:
            return "🔺 Slipped"
        if row["Variance (days)"] < 0:
            return "🔻 Improved"
        return "➖ No Change"

    df["Trend"] = df.apply(trend, axis=1)

    # -------------------------
    # STATUS ENGINE (KEY FIX)
    # -------------------------
    def status(row):
        if pd.isna(row["CL32 Finish"]):
            return "🟡 No Update"

        v = row["Variance (days)"]

        if v >= 7:
            return "🔴 Critical Delay"
        if v >= 3:
            return "🟠 At Risk"
        if v > -3:
            return "🟡 Monitor"
        return "🟢 Ahead"

    df["Status"] = df.apply(status, axis=1)

    # -------------------------
    # FLOAT (placeholder if missing)
    # -------------------------
    df["Float"] = df.get("Float", "")

    # -------------------------
    # FINAL OUTPUT TABLE
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