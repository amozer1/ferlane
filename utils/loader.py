import pandas as pd
import numpy as np


# ---------------------------
# DATE CLEANING
# ---------------------------
def parse_date(val):
    if pd.isna(val):
        return pd.NaT

    val = str(val).strip()

    # remove artifacts like * or A
    val = val.replace("*", "").replace(" A", "").strip()

    return pd.to_datetime(val, errors="coerce")


def format_date(val):
    if pd.isna(val):
        return None
    return pd.to_datetime(val).strftime("%d-%b-%Y")


# ---------------------------
# LOAD DATA
# ---------------------------
def load_file(file_path):
    df = pd.read_excel(file_path)

    df.columns = [c.strip() for c in df.columns]

    # standardise expected columns
    df = df.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": "Finish"
    })

    df["Deliverable"] = df["Deliverable"].astype(str).str.strip()

    df["Finish"] = df["Finish"].apply(parse_date)

    # remove invalid rows
    df = df[~df["Deliverable"].isin(["nan", "", "None"])]
    df = df.dropna(subset=["Deliverable"])

    # keep last occurrence if duplicates exist
    df = df.sort_values("Finish").groupby("Deliverable", as_index=False).last()

    return df


# ---------------------------
# COMPARE FUNCTION
# ---------------------------
def prepare_comparison_df(df31, df32):

    cl31 = df31.set_index("Deliverable")["Finish"]
    cl32 = df32.set_index("Deliverable")["Finish"]

    all_keys = sorted(set(cl31.index).union(set(cl32.index)))

    rows = []

    for d in all_keys:
        v31 = cl31.get(d, pd.NaT)
        v32 = cl32.get(d, pd.NaT)

        # skip if both empty
        if pd.isna(v31) and pd.isna(v32):
            continue

        # determine change type
        if pd.notna(v31) and pd.isna(v32):
            change = "REMOVED"
        elif pd.isna(v31) and pd.notna(v32):
            change = "NEW"
        else:
            change = "MODIFIED" if v31 != v32 else "UNCHANGED"

        # delta
        if pd.notna(v31) and pd.notna(v32):
            delta = (v32 - v31).days
        else:
            delta = None

        # status
        if change == "NEW":
            status = "Added in CL32"
        elif change == "REMOVED":
            status = "Dropped from CL32"
        elif change == "UNCHANGED":
            status = "No change"
        else:
            status = (
                "Delayed" if delta and delta > 0 else
                "Early" if delta and delta < 0 else
                "No change"
            )

        rows.append({
            "Deliverable": d,
            "CL31 Finish": format_date(v31),
            "CL32 Finish": format_date(v32),
            "Delta (Days)": delta,
            "Change Type": change,
            "Status / Comment": status
        })

    return pd.DataFrame(rows)