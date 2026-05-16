```python id="pwjlwm"
# utils/deliverables.py

import pandas as pd
import numpy as np


# ---------------------------------------------------
# CLEAN NAMES
# ---------------------------------------------------

def clean_name(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    return value


# ---------------------------------------------------
# CHANGE TYPE
# ---------------------------------------------------

def determine_change_type(cl31, cl32, delta):

    # NEW IN CL32
    if pd.isna(cl31) and pd.notna(cl32):
        return "NEW"

    # REMOVED FROM CL32
    if pd.notna(cl31) and pd.isna(cl32):
        return "REMOVED"

    # BOTH EXIST
    if pd.notna(delta):

        if delta > 0:
            return "DELAYED"

        elif delta < 0:
            return "ACCELERATED"

        else:
            return "ON TRACK"

    return "UNKNOWN"


# ---------------------------------------------------
# COMMENTS
# ---------------------------------------------------

def status_comment(change_type):

    comments = {
        "DELAYED": "Shifted later than previous programme",
        "ACCELERATED": "Earlier than previous programme",
        "ON TRACK": "No change",
        "NEW": "Added in latest programme",
        "REMOVED": "Removed from latest programme"
    }

    return comments.get(change_type, "")


# ---------------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------------

def build_deliverables_table(df31, df32):

    # -------------------------------------------
    # COPY
    # -------------------------------------------

    df31 = df31.copy()
    df32 = df32.copy()

    # -------------------------------------------
    # CLEAN ACTIVITY NAMES
    # -------------------------------------------

    df31["Activity Name"] = df31["Activity Name"].apply(clean_name)
    df32["Activity Name"] = df32["Activity Name"].apply(clean_name)

    df31 = df31[df31["Activity Name"].notna()]
    df32 = df32[df32["Activity Name"].notna()]

    # -------------------------------------------
    # KEEP ONLY REQUIRED COLUMNS
    # -------------------------------------------

    cl31 = df31[
        ["Activity Name", "Finish"]
    ].rename(
        columns={
            "Finish": "CL31 Finish"
        }
    )

    cl32 = df32[
        ["Activity Name", "Finish"]
    ].rename(
        columns={
            "Finish": "CL32 Finish"
        }
    )

    # -------------------------------------------
    # MERGE
    # -------------------------------------------

    merged = pd.merge(
        cl31,
        cl32,
        on="Activity Name",
        how="outer"
    )

    # -------------------------------------------
    # DATE CONVERSION
    # -------------------------------------------

    merged["CL31 Finish"] = pd.to_datetime(
        merged["CL31 Finish"],
        errors="coerce"
    )

    merged["CL32 Finish"] = pd.to_datetime(
        merged["CL32 Finish"],
        errors="coerce"
    )

    # -------------------------------------------
    # DELTA
    # -------------------------------------------

    merged["Delta (Days)"] = (
        merged["CL32 Finish"] - merged["CL31 Finish"]
    ).dt.days

    # -------------------------------------------
    # CHANGE TYPE
    # -------------------------------------------

    merged["Change Type"] = merged.apply(
        lambda row: determine_change_type(
            row["CL31 Finish"],
            row["CL32 Finish"],
            row["Delta (Days)"]
        ),
        axis=1
    )

    # -------------------------------------------
    # STATUS COMMENTS
    # -------------------------------------------

    merged["Status / Comment"] = merged[
        "Change Type"
    ].apply(status_comment)

    # -------------------------------------------
    # FORMAT DATES
    # -------------------------------------------

    merged["CL31 Finish"] = merged[
        "CL31 Finish"
    ].dt.strftime("%d-%b-%y")

    merged["CL32 Finish"] = merged[
        "CL32 Finish"
    ].dt.strftime("%d-%b-%y")

    merged = merged.fillna("—")

    # -------------------------------------------
    # FINAL COLUMN NAMES
    # -------------------------------------------

    merged = merged.rename(
        columns={
            "Activity Name": "Deliverable"
        }
    )

    # -------------------------------------------
    # SORTING
    # -------------------------------------------

    order = {
        "DELAYED": 1,
        "ACCELERATED": 2,
        "NEW": 3,
        "REMOVED": 4,
        "ON TRACK": 5
    }

    merged["Sort"] = merged["Change Type"].map(order)

    merged = merged.sort_values(
        by=["Sort", "Deliverable"]
    )

    merged.drop(columns=["Sort"], inplace=True)

    merged.reset_index(drop=True, inplace=True)

    return merged
```
