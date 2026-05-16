import pandas as pd


def _to_date(series):
    return pd.to_datetime(series, errors="coerce")


def build_deliverables(cl31, cl32):

    cl31 = cl31.copy()
    cl32 = cl32.copy()

    # =========================
    # KEEP RAW DATES (NO FORMATTING YET)
    # =========================
    cl31["Deliverable"] = cl31["Activity Name"]
    cl31["CL31 Finish_raw"] = _to_date(cl31["BL Project Finish"])

    cl32["Deliverable"] = cl32["Activity Name"]
    cl32["CL32 Finish_raw"] = _to_date(cl32["Finish"])

    # =========================
    # MERGE
    # =========================
    df = cl31[["Deliverable", "CL31 Finish_raw"]].merge(
        cl32[["Deliverable", "CL32 Finish_raw"]],
        on="Deliverable",
        how="outer"
    )

    # =========================
    # PRESERVE ORDER
    # =========================
    order = cl31["Deliverable"].tolist()

    df["__order"] = df["Deliverable"].apply(
        lambda x: order.index(x) if x in order else 10**9
    )

    df = df.sort_values("__order").drop(columns="__order")

    # =========================
    # DELTA (CLEAN + SAFE)
    # =========================
    def calc_delta(row):
        if pd.isna(row["CL31 Finish_raw"]) or pd.isna(row["CL32 Finish_raw"]):
            return pd.NA
        return (row["CL32 Finish_raw"] - row["CL31 Finish_raw"]).days

    df["Delta (Days)"] = df.apply(calc_delta, axis=1).astype("Int64")

    # =========================
    # CHANGE TYPE
    # =========================
    def change(row):
        if pd.isna(row["CL31 Finish_raw"]) and pd.notna(row["CL32 Finish_raw"]):
            return "NEW"
        if pd.notna(row["CL31 Finish_raw"]) and pd.isna(row["CL32 Finish_raw"]):
            return "REMOVED"
        if pd.isna(row["Delta (Days)"]):
            return "UNCHANGED"
        if row["Delta (Days)"] > 0:
            return "DELAYED"
        if row["Delta (Days)"] < 0:
            return "EARLY"
        return "UNCHANGED"

    df["Change Type"] = df.apply(change, axis=1)

    # =========================
    # COMMENT
    # =========================
    def comment(x):
        if x == "NEW":
            return "Added scope in CL32"
        if x == "REMOVED":
            return "Removed from CL32"
        if x == "DELAYED":
            return "Shifted later, coordination required"
        if x == "EARLY":
            return "Pulled forward"
        return "Stable"

    df["Status / Comment"] = df["Change Type"].apply(comment)

    # =========================
    # FINAL FORMAT (ONLY NOW)
    # =========================
    def fmt(x):
        return "-" if pd.isna(x) else x.strftime("%d-%b-%y")

    df["CL31 Finish"] = df["CL31 Finish_raw"].apply(fmt)
    df["CL32 Finish"] = df["CL32 Finish_raw"].apply(fmt)

    df = df.drop(columns=["CL31 Finish_raw", "CL32 Finish_raw"])

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