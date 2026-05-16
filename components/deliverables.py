import pandas as pd


def build_deliverables_card(cl31: pd.DataFrame, cl32: pd.DataFrame):

    # -------------------------
    # KEEP ONLY REQUIRED FIELDS
    # -------------------------
    cl31 = cl31[["Activity Name", "Start", "Finish"]].copy()
    cl32 = cl32[["Activity Name", "Start", "Finish"]].copy()

    cl31 = cl31.rename(columns={
        "Start": "CL31 Start",
        "Finish": "CL31 Finish"
    })

    cl32 = cl32.rename(columns={
        "Start": "CL32 Start",
        "Finish": "CL32 Finish"
    })

    # -------------------------
    # MERGE BY ACTIVITY NAME
    # -------------------------
    df = pd.merge(cl31, cl32, on="Activity Name", how="outer")

    # -------------------------
    # CONVERT TO DATETIME (SAFE)
    # -------------------------
    for col in ["CL31 Start", "CL31 Finish", "CL32 Start", "CL32 Finish"]:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

    # -------------------------
    # DELTA CALCULATIONS
    # -------------------------
    df["Δ Start (Days)"] = (df["CL32 Start"] - df["CL31 Start"]).dt.days
    df["Δ Finish (Days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

    # -------------------------
    # STATUS LOGIC
    # -------------------------
    def status(row):
        if pd.isna(row["Δ Finish (Days)"]) and pd.isna(row["Δ Start (Days)"]):
            return "⚪ No Change"

        if (row["Δ Finish (Days)"] or 0) > 20:
            return "🔴 Major Delay"

        if (row["Δ Finish (Days)"] or 0) > 0 or (row["Δ Start (Days)"] or 0) > 0:
            return "🔴 Changed (Delayed)"

        if (row["Δ Finish (Days)"] or 0) < 0:
            return "🟢 Improved"

        return "🟡 Minor Change"

    df["Status"] = df.apply(status, axis=1)

    # -------------------------
    # FINAL OUTPUT FORMAT
    # -------------------------
    df["CL31 Start"] = df["CL31 Start"].dt.strftime("%d-%b-%Y")
    df["CL31 Finish"] = df["CL31 Finish"].dt.strftime("%d-%b-%Y")
    df["CL32 Start"] = df["CL32 Start"].dt.strftime("%d-%b-%Y")
    df["CL32 Finish"] = df["CL32 Finish"].dt.strftime("%d-%b-%Y")

    return df[[
        "Activity Name",
        "CL31 Start",
        "CL32 Start",
        "CL31 Finish",
        "CL32 Finish",
        "Δ Start (Days)",
        "Δ Finish (Days)",
        "Status"
    ]]