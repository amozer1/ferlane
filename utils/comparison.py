def build_variance_table(cl31, cl32):
    """
    Align CL31 vs CL32 datasets
    """

    df = cl31.merge(
        cl32,
        on="Activity ID",
        suffixes=("_cl31", "_cl32"),
        how="outer"
    )

    df["Deliverable"] = df.get("Activity Name_cl31", df.get("Activity Name_cl32"))

    # Safe date mapping
    df["CL31 Finish"] = df.get("Finish_cl31")
    df["CL32 Finish"] = df.get("Finish_cl32")

    # Variance (if available)
    df["Delta_Days"] = df.get("Variance - BL1 Finish Date", 0)
    df["Float"] = df.get("Total Float", 0)

    return df