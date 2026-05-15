def calculate_deltas(df):

    # ============================================
    # FINISH DELTA
    # ============================================

    df["Delta Finish Days"] = (
        df["Finish_32"] - df["Finish_31"]
    ).dt.days

    # ============================================
    # START DELTA
    # ============================================

    df["Delta Start Days"] = (
        df["Start_32"] - df["Start_31"]
    ).dt.days

    # ============================================
    # FLOAT VARIANCE
    # ============================================

    df["Float Variance"] = (
        df["Total Float_32"] -
        df["Total Float_31"]
    )

    return df