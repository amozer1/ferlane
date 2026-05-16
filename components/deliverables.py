import pandas as pd


def extract_deliverables(df: pd.DataFrame) -> pd.DataFrame:
    """
    Treats ALL leaf-level activities as deliverables dynamically.
    No hardcoding of names.
    """

    df = df.copy()

    # Ensure required columns exist
    required = ["id", "name", "finish", "bl_finish"]
    for r in required:
        if r not in df.columns:
            raise ValueError(f"Missing column: {r}")

    # Identify deliverables (leaf tasks)
    df["is_deliverable"] = (
        df["id"].astype(str).str.contains(r"^[A-Z]{2,}-", na=False)
    ) & (df["name"].notna())

    deliverables = df[df["is_deliverable"]].copy()

    # Remove empty rows
    deliverables = deliverables[deliverables["name"].str.len() > 0]

    return deliverables


def compare_cl31_cl32(df31: pd.DataFrame, df32: pd.DataFrame) -> pd.DataFrame:
    """
    Compare CL31 vs CL32 deliverables dynamically.
    """

    df31 = df31.set_index("id")
    df32 = df32.set_index("id")

    all_ids = sorted(set(df31.index) | set(df32.index))

    rows = []

    for _id in all_ids:
        a = df31.loc[_id] if _id in df31.index else None
        b = df32.loc[_id] if _id in df32.index else None

        cl31_finish = a["finish"] if a is not None else None
        cl32_finish = b["finish"] if b is not None else None

        # Delta logic
        if pd.notna(cl31_finish) and pd.notna(cl32_finish):
            delta = (cl32_finish - cl31_finish).days
            change = "DELAYED" if delta > 0 else "AHEAD" if delta < 0 else "UNCHANGED"
        elif pd.isna(cl31_finish) and pd.notna(cl32_finish):
            delta = "NEW"
            change = "NEW"
        elif pd.notna(cl31_finish) and pd.isna(cl32_finish):
            delta = "REMOVED"
            change = "REMOVED"
        else:
            delta = None
            change = None

        rows.append({
            "Deliverable": (_id if _id else "UNKNOWN"),
            "CL31 Finish": cl31_finish,
            "CL32 Finish": cl32_finish,
            "Delta (Days)": delta,
            "Change Type": change,
        })

    return pd.DataFrame(rows)