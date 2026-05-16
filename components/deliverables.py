import pandas as pd


def extract_deliverables(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=["Activity Name"])
    df["Activity Name"] = df["Activity Name"].astype(str).str.strip()
    return df


def build_deliverables_card(df: pd.DataFrame) -> pd.DataFrame:

    out = df.copy()

    out["Δ Finish (Days)"] = (
        pd.to_datetime(out["Finish"], dayfirst=True)
        - pd.to_datetime(out["BL Finish"], dayfirst=True)
    ).dt.days

    def status(x):
        if pd.isna(x):
            return "⚪ Unknown"
        if x > 20:
            return "🔴 Critical"
        if x > 0:
            return "🔴 Delayed"
        if x < -10:
            return "🟢 Ahead"
        return "🟡 At Risk"

    out["Status"] = out["Δ Finish (Days)"].apply(status)

    return out[[
        "Activity Name",
        "Start",
        "Finish",
        "BL Start",
        "BL Finish",
        "Δ Finish (Days)",
        "Status"
    ]]