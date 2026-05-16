# deliverables.py

import pandas as pd
import numpy as np


def build_deliverables(cl31, cl32):

    cl31 = cl31.copy()
    cl32 = cl32.copy()

    # ---------------------------------------------------
    # CLEAN COLUMN NAMES
    # ---------------------------------------------------

    cl31.columns = cl31.columns.str.strip()
    cl32.columns = cl32.columns.str.strip()

    # ---------------------------------------------------
    # STANDARDISE
    # ---------------------------------------------------

    cl31 = cl31.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": "CL31 Finish",
        "Total Float": "CL31 Float"
    })

    cl32 = cl32.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": "CL32 Finish",
        "Total Float": "CL32 Float"
    })

    # ---------------------------------------------------
    # KEEP REQUIRED FIELDS
    # ---------------------------------------------------

    cl31 = cl31[
        [
            "Deliverable",
            "CL31 Finish",
            "CL31 Float"
        ]
    ]

    cl32 = cl32[
        [
            "Deliverable",
            "CL32 Finish",
            "CL32 Float"
        ]
    ]

    # ---------------------------------------------------
    # REMOVE BLANKS
    # ---------------------------------------------------

    cl31["Deliverable"] = (
        cl31["Deliverable"]
        .astype(str)
        .str.strip()
    )

    cl32["Deliverable"] = (
        cl32["Deliverable"]
        .astype(str)
        .str.strip()
    )

    cl31 = cl31[
        cl31["Deliverable"] != ""
    ]

    cl32 = cl32[
        cl32["Deliverable"] != ""
    ]

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    cl31 = cl31.drop_duplicates(
        subset=["Deliverable"]
    )

    cl32 = cl32.drop_duplicates(
        subset=["Deliverable"]
    )

    # ---------------------------------------------------
    # MERGE
    # ---------------------------------------------------

    df = pd.merge(
        cl31,
        cl32,
        on="Deliverable",
        how="outer"
    )

    # ---------------------------------------------------
    # DATES
    # ---------------------------------------------------

    df["CL31 Finish"] = pd.to_datetime(
        df["CL31 Finish"],
        errors="coerce"
    )

    df["CL32 Finish"] = pd.to_datetime(
        df["CL32 Finish"],
        errors="coerce"
    )

    # ---------------------------------------------------
    # FLOAT
    # ---------------------------------------------------

    df["Float"] = df["CL32 Float"]

    # ---------------------------------------------------
    # DELTA
    # ---------------------------------------------------

    df["Delta (Days)"] = (
        df["CL32 Finish"] -
        df["CL31 Finish"]
    ).dt.days

    # ---------------------------------------------------
    # CHANGE TYPE
    # ---------------------------------------------------

    def classify(row):

        cl31_missing = pd.isna(row["CL31 Finish"])
        cl32_missing = pd.isna(row["CL32 Finish"])

        if cl31_missing and not cl32_missing:
            return "NEW"

        if not cl31_missing and cl32_missing:
            return "REMOVED"

        if row["Delta (Days)"] == 0:
            return "UNCHANGED"

        if row["Delta (Days)"] > 0:
            return "DELAYED"

        if row["Delta (Days)"] < 0:
            return "EARLY"

        return "UNCHANGED"

    df["Change Type"] = df.apply(
        classify,
        axis=1
    )

    # ---------------------------------------------------
    # COMMENTS
    # ---------------------------------------------------

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

    df["Status / Comment"] = df.apply(
        comment,
        axis=1
    )

    # ---------------------------------------------------
    # DATE FORMAT
    # ---------------------------------------------------

    df["CL31 Finish"] = df["CL31 Finish"].dt.strftime(
        "%d-%b-%y"
    )

    df["CL32 Finish"] = df["CL32 Finish"].dt.strftime(
        "%d-%b-%y"
    )

    # ---------------------------------------------------
    # FINAL ORDER
    # ---------------------------------------------------

    df = df[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Float",
            "Change Type",
            "Status / Comment"
        ]
    ]

    # ---------------------------------------------------
    # SORT
    # ---------------------------------------------------

    order = {
        "DELAYED": 1,
        "EARLY": 2,
        "NEW": 3,
        "REMOVED": 4,
        "UNCHANGED": 5
    }

    df["Sort"] = df["Change Type"].map(order)

    df = df.sort_values(
        by=["Sort", "Delta (Days)"],
        ascending=[True, False]
    )

    df = df.drop(columns=["Sort"])

    return df.reset_index(drop=True)