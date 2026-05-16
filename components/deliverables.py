import pandas as pd


def extract_deliverables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deliverables = Activity Name ONLY (no hierarchy, no mapping)
    """

    deliverables = df.copy()

    deliverables = deliverables.dropna(subset=["Activity Name"])

    deliverables["Activity Name"] = deliverables["Activity Name"].astype(str).str.strip()

    return deliverables


def build_deliverables_card(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build comparison table:
    CL logic must already be handled in loader
    """

    out = df.copy()

    # variance calculation (simple)
    out["Δ Finish (Days)"] = (
        pd.to_datetime(out["Finish"], dayfirst=True)
        - pd.to_datetime(out["BL Finish"], dayfirst=True)
    ).dt.days

    out["Status"] = out["Δ Finish (Days)"].apply(lambda x:
        "🔴 Critical" if x > 20 else
        "🔴 Delayed" if x > 0 else
        "🟡 At Risk" if x > -10 else
        "🟢 On Track"
    )

    return out[[
        "Activity Name",
        "Start",
        "Finish",
        "BL Start",
        "BL Finish",
        "Δ Finish (Days)",
        "Status"
    ]]