def compute_kpis(df):

    total = len(df)
    critical = len(df[df["Status"] == "Critical"])
    near = len(df[df["Status"] == "Near Critical"])
    non = len(df[df["Status"] == "Non Critical"])

    avg_float = df["Float"].mean()

    return {
        "total": total,
        "critical": critical,
        "near_critical": near,
        "non_critical": non,
        "avg_float": avg_float
    }