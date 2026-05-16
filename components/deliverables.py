import pandas as pd

def _safe_date(df, col):
    if col in df.columns:
        return pd.to_datetime(df[col], errors="coerce")
    return pd.NaT


def build_design_control_table(cl31: pd.DataFrame, cl32: pd.DataFrame) -> pd.DataFrame:
    """
    Builds CL31 vs CL32 comparison table for design management control.
    """

    # -------------------------
    # KEEP ONLY ESSENTIAL FIELDS (SAFE FALLBACK)
    # -------------------------
    base_cols = ["Activity ID", "Activity Name"]

    cl31 = cl31.copy()
    cl32 = cl32.copy()

    # standardise column names
    cl31.columns = cl31.columns.str.strip()
    cl32.columns = cl32.columns.str.strip()

    # -------------------------
    # MERGE
    # -------------------------
    df = cl31.merge(
        cl32,
        on="Activity ID",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    # -------------------------
    # FINISH DATES
    # -------------------------
    cl31_finish = _safe_date(df, "Finish_CL31")
    cl32_finish = _safe_date(df, "Finish_CL32")

    df["CL31 Finish"] = cl31_finish
    df["CL32 Finish"] = cl32_finish

    # -------------------------
    # VARIANCE
    # -------------------------
    df["Variance (days)"] = (df["CL32 Finish"] - df["CL31 Finish"]).dt.days

    # -------------------------
    # DISCIPLINE (DERIVED IF NOT PRESENT)
    # -------------------------
    if "Discipline" not in df.columns:
        def assign_discipline(name):
            if pd.isna(name):
                return "Unknown"
            name = str(name).lower()
            if "meica" in name or "electrical" in name:
                return "MEICA"
            if "civil" in name or "shaft" in name:
                return "Civils"
            if "procure" in name:
                return "Procurement"
            if "design" in name:
                return "Design"
            return "General"

        df["Discipline"] = df["Activity Name_CL31"].apply(assign_discipline)

    # -------------------------
    # STATUS LOGIC
    # -------------------------
    def status(v):
        if pd.isna(v):
            return "🟡 No Data"
        if v <= 0:
            return "🟢 On Track"
        elif v <= 5:
            return "🟡 Minor Delay"
        elif v <= 15:
            return "🟠 At Risk"
        else:
            return "🔴 Critical Delay"

    df["Status"] = df["Variance (days)"].apply(status)

    # -------------------------
    # FLOAT (if exists)
    # -------------------------
    if "Total Float_CL32" in df.columns:
        df["Float"] = df["Total Float_CL32"]
    else:
        df["Float"] = 0

    # -------------------------
    # FINAL CLEAN TABLE
    # -------------------------
    final_cols = [
        "Activity ID",
        "Activity Name_CL31",
        "Discipline",
        "CL31 Finish",
        "CL32 Finish",
        "Variance (days)",
        "Float",
        "Status"
    ]

    return df[[c for c in final_cols if c in df.columns]]