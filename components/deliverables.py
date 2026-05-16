import pandas as pd

def build_design_control_table(cl31, cl32):

    # -------------------------
    # MERGE
    # -------------------------
    df = pd.merge(
        cl32,
        cl31[["Activity ID", "CL31 Finish", "CL31 Float"]],
        on="Activity ID",
        how="left"
    )

    # -------------------------
    # DATE CONVERSION
    # -------------------------
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"], errors="coerce")
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"], errors="coerce")

    # -------------------------
    # DELTAS
    # -------------------------
    df["Finish Δ (days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days
    df["Float Δ"] = df["CL32 Float"] - df["CL31 Float"]

    # -------------------------
    # RISK LOGIC
    # -------------------------
    def status(row):
        if pd.isna(row["Finish Δ (days)"]):
            return "⚪ No Data"

        if row["CL32 Float"] <= 0 or row["Finish Δ (days)"] > 3:
            return "🔴 Critical"

        if row["Finish Δ (days)"] > 1 or row["Float Δ"] < 0:
            return "🟠 At Risk"

        if row["Finish Δ (days)"] == 0:
            return "🟢 Stable"

        return "🟡 Watch"

    df["Status"] = df.apply(status, axis=1)

    # -------------------------
    # ACTION ENGINE
    # -------------------------
    def action(x):
        if "🔴" in x:
            return "Escalate"
        if "🟠" in x:
            return "Monitor"
        if "🟡" in x:
            return "Review"
        return "None"

    df["Action"] = df["Status"].apply(action)

    # -------------------------
    # FINAL TABLE
    # -------------------------
    return df[[
        "Activity ID",
        "Activity Name",
        "Discipline",
        "CL31 Finish",
        "CL32 Finish",
        "Finish Δ (days)",
        "CL31 Float",
        "CL32 Float",
        "Float Δ",
        "Status",
        "Action"
    ]]