# components/dashboard.py

import pandas as pd
from datetime import datetime


def build_dashboard_card(df31, df32):

    # -------------------------
    # STANDARDISE INPUTS
    # -------------------------
    df31 = df31.copy()
    df32 = df32.copy()

    df31 = df31[["Activity Name", "Finish_Eff"]].dropna()
    df32 = df32[["Activity Name", "Finish_Eff"]].dropna()

    df31.columns = ["Deliverable", "CL31 Finish"]
    df32.columns = ["Deliverable", "CL32 Finish"]

    merged = pd.merge(df31, df32, on="Deliverable", how="outer")

    # -------------------------
    # DATE CONVERSION
    # -------------------------
    merged["CL31 Finish"] = pd.to_datetime(merged["CL31 Finish"], errors="coerce")
    merged["CL32 Finish"] = pd.to_datetime(merged["CL32 Finish"], errors="coerce")

    # -------------------------
    # DELTA CALCULATION
    # -------------------------
    merged["Δ Finish (Days)"] = (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days

    # -------------------------
    # FLOAT LOGIC (simple proxy)
    # -------------------------
    merged["Float Change"] = merged["Δ Finish (Days)"].fillna(0)

    # -------------------------
    # STATUS RULES (NEC STYLE)
    # -------------------------
    def status(row):
        delta = row["Δ Finish (Days)"]

        if pd.isna(delta):
            return "🟣 Missing Data"
        elif delta <= 0:
            return "🟢 On Track / Ahead"
        elif delta <= 10:
            return "🟡 At Risk"
        else:
            return "🔴 Critical Delay"

    merged["Status"] = merged.apply(status, axis=1)

    # -------------------------
    # FORMAT OUTPUT DATES
    # -------------------------
    merged["CL31 Finish"] = merged["CL31 Finish"].dt.strftime("%d-%b-%Y")
    merged["CL32 Finish"] = merged["CL32 Finish"].dt.strftime("%d-%b-%Y")

    return merged[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Δ Finish (Days)",
        "Float Change",
        "Status"
    ]]