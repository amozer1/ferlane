import pandas as pd
from components.deliverables import build_deliverable_summary


# -----------------------------
# LOAD + CLEAN FILES
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

    # Standardise column names (safe guard)
    df.columns = [c.strip() for c in df.columns]

    # Ensure required columns exist
    required_cols = ["Activity Name", "Finish"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # Clean finish dates (remove A, *, spaces)
    df["Finish"] = (
        df["Finish"]
        .astype(str)
        .str.replace(r"[A*]", "", regex=True)
        .str.strip()
    )

    # Convert to datetime
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # Remove invalid rows (your requirement)
    df = df.dropna(subset=["Finish"])

    # Create Deliverable (LEVEL = summary grouping)
    df["Deliverable"] = df["Activity Name"].apply(extract_deliverable)

    return df


# -----------------------------
# EXTRACT DELIVERABLE
# -----------------------------
def extract_deliverable(name):

    if pd.isna(name):
        return None

    name = str(name).strip()

    # Ignore task-level IDs
    if "-" in name[:15] and any(x.isdigit() for x in name[:10]):
        return None

    # Heuristic: treat summary rows as deliverables
    summary_keywords = [
        "Design",
        "Modelling",
        "Review",
        "Dates",
        "Deliverables",
        "Shaft",
        "EICA",
        "Mechanical",
        "Civils",
        "Process",
        "Geotechnical"
    ]

    for k in summary_keywords:
        if k.lower() in name.lower():
            return name

    return None


# -----------------------------
# COMPARE CL31 vs CL32
# -----------------------------
def prepare_comparison_df(df31, df32):

    cl31 = build_deliverable_summary(df31).rename(columns={"Finish": "CL31 Finish"})
    cl32 = build_deliverable_summary(df32).rename(columns={"Finish": "CL32 Finish"})

    merged = cl31.merge(cl32, on="Deliverable", how="outer")

    # Delta
    merged["Delta (Days)"] = (
        (merged["CL32 Finish"] - merged["CL31 Finish"]).dt.days
    )

    # Change Type
    def change_type(r):
        if pd.isna(r["CL31 Finish"]):
            return "NEW"
        if pd.isna(r["CL32 Finish"]):
            return "REMOVED"
        if r["Delta (Days)"] == 0:
            return "UNCHANGED"
        return "MODIFIED"

    merged["Change Type"] = merged.apply(change_type, axis=1)

    # Status
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

    # Final formatting
    merged = merged[
        [
            "Deliverable",
            "CL31 Finish",
            "CL32 Finish",
            "Delta (Days)",
            "Change Type",
            "Status / Comment"
        ]
    ]

    return merged