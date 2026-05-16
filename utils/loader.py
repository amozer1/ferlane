import pandas as pd
from components.deliverables import build_deliverable_summary


# -----------------------------
# LOAD FILES (AUTO OR UPLOAD)
# -----------------------------
def load_and_prepare_files(file31, file32):

    df31 = pd.read_excel(file31)
    df32 = pd.read_excel(file32)

    df31 = clean_dataframe(df31)
    df32 = clean_dataframe(df32)

    return df31, df32


# -----------------------------
# CLEAN DATAFRAME
# -----------------------------
def clean_dataframe(df):
    df = df.copy()

    df.columns = [c.strip() for c in df.columns]

    if "Activity Name" not in df.columns:
        df["Activity Name"] = None
    if "Finish" not in df.columns:
        df["Finish"] = None

    df["Finish"] = (
        df["Finish"]
        .astype(str)
        .str.replace(r"[A*]", "", regex=True)
        .str.strip()
    )

    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # remove invalid dates (your rule)
    df = df.dropna(subset=["Finish"])

    df["Deliverable"] = df["Activity Name"].apply(extract_deliverable)

    return df


# -----------------------------
# DELIVERABLE EXTRACTION
# -----------------------------
def extract_deliverable(name):

    if pd.isna(name):
        return None

    name = str(name).strip()

    # ignore task-level IDs
    if "-" in name[:15] and any(char.isdigit() for char in name[:10]):
        return None

    keywords = [
        "Design",
        "Modelling",
        "Review",
        "Deliverables",
        "Shaft",
        "EICA",
        "Mechanical",
        "Civils",
        "Process",
        "Geotechnical",
        "Dates"
    ]

    for k in keywords:
        if k.lower() in name.lower():
            return name

    return None


# -----------------------------
# COMPARISON LOGIC
# -----------------------------
def prepare_comparison_df(df31, df32):

    cl31 = build_deliverable_summary(df31).rename(columns={"Finish": "CL31 Finish"})
    cl32 = build_deliverable_summary(df32).rename(columns={"Finish": "CL32 Finish"})

    merged = cl31.merge(cl32, on="Deliverable", how="outer")

    merged["Delta (Days)"] = (
        (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days
    )

    def change_type(r):
        if pd.isna(r["CL31 Finish"]):
            return "NEW"
        if pd.isna(r["CL32 Finish"]):
            return "REMOVED"
        if r["Delta (Days)"] == 0:
            return "UNCHANGED"
        return "MODIFIED"

    merged["Change Type"] = merged.apply(change_type, axis=1)

    def status(r):
        if r["Change Type"] == "NEW":
            return "Added in CL32"
        if r["Change Type"] == "REMOVED":
            return "Dropped from CL32"
        if r["Change Type"] == "UNCHANGED":
            return "Stable"

        d = r["Delta (Days)"]
        if pd.notna(d) and d > 0:
            return "Delayed vs CL31 baseline"
        if pd.notna(d) and d < 0:
            return "Pulled forward"

        return "Updated"

    merged["Status / Comment"] = merged.apply(status, axis=1)

    return merged[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Change Type",
            "Status / Comment"
        ]
    ]