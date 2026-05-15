import numpy as np

def compute_kpis(df):
    """
    Computes executive KPI metrics for dashboard
    """

    total = len(df)

    critical = len(df[df["Status"] == "Critical"])
    near_critical = len(df[df["Status"] == "Near Critical"])
    on_track = len(df[df["Status"] == "On Track"])

    avg_float = df["Float"].replace([np.inf, -np.inf], np.nan).fillna(0).mean()

    return {
        "total": total,
        "critical": critical,
        "near_critical": near_critical,
        "non_critical": on_track,
        "avg_float": avg_float
    }