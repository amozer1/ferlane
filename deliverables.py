import pandas as pd


def _to_date(series):
    return pd.to_datetime(series, errors="coerce")


def build_deliverables(cl31, cl32):

    cl31 = cl31.copy()
    cl32 = cl32.copy()

    # =========================
    # CL31 (ONLY BL Project Finish)
    # =========================
    cl31["Deliverable"] = cl31["Activity Name"]
    cl31["CL31 Finish"] = _to_date(cl31["BL Project Finish"])
    cl31 = cl31[["Deliverable", "CL31 Finish"]]


    # =========================
    # CL32 (ONLY Finish)
    # =========================
    cl32["Deliverable"] = cl32["Activity Name"]
    cl32["CL32 Finish"] = _to_date(cl32["Finish"])
    cl32 = cl32[["Deliverable", "CL32 Finish"]]


    # =========================
    # MERGE
    # =========================
    df = cl31.merge(cl32, on="Deliverable", how="outer")


    # =========================
    # PRESERVE CL31 ORDER + APPEND NEW
    # =========================
    cl31_order = cl31["Deliverable"].tolist()

    def order_func(x):
        try:
            return cl31_order.index(x)
        except:
            return 10**9

    df["__order"] = df["Deliverable"].apply(order_func)
    df = df.sort_values("__order").drop(columns="__order")


    # =========================
    # FORMAT DATES
    # =========================
    def fmt(x):
        if pd.isna(x):
            return "-"
        return pd.to_datetime(x).strftime("%d-%b-%y")


    df["CL31 Finish"] = df["CL31 Finish"].apply(fmt)
    df["CL32 Finish"] = df["CL32 Finish"].apply(fmt)


    # =========================
    # DELTA
    # =========================
    def delta(row):
        if row["CL31 Finish"] == "-" or row["CL32 Finish"] == "-":
            return None
        try:
            d1 = pd.to_datetime(row["CL31 Finish"])
            d2 = pd.to_datetime(row["CL32 Finish"])
            return (d2 - d1).days
        except:
            return None


    df["Delta (Days)"] = df.apply(delta, axis=1)


    # =========================
    # CHANGE TYPE
    # =========================
    def change(row):
        if row["CL31 Finish"] == "-" and row["CL32 Finish"] != "-":
            return "NEW"
        if row["CL31 Finish"] != "-" and row["CL32 Finish"] == "-":
            return "REMOVED"
        if row["Delta (Days)"] is None:
            return "UNCHANGED"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] < 0:
            return "EARLY"
        return "UNCHANGED"


    df["Change Type"] = df.apply(change, axis=1)


    # =========================
    # STATUS COMMENT
    # =========================
    def comment(row):
        if row["Change Type"] == "NEW":
            return "Added scope in CL32"
        if row["Change Type"] == "REMOVED":
            return "Removed from CL32"
        if row["Change Type"] == "DELAYED":
            return "Shifted later, coordination required"
        if row["Change Type"] == "EARLY":
            return "Pulled forward"
        return "Stable"


    df["Status / Comment"] = df.apply(comment, axis=1)


    # =========================
    # FINAL OUTPUT
    # =========================
    return df[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Change Type",
            "Status / Comment"
        ]
    ]