# deliverables.py
import pandas as pd
import re


# -----------------------------
# DETECT DELIVERABLES
# -----------------------------
def is_deliverable(text: str) -> bool:
    if not isinstance(text, str):
        return False

    t = text.lower()

    include_keywords = [
        "submission", "design", "report", "drawing", "plan",
        "schedule", "assessment", "specification", "model",
        "analysis", "register", "philosophy", "calculation",
        "package", "ga", "p&id", "p&ids", "document"
    ]

    exclude_keywords = [
        "review", "meeting", "mobilisation", "raise",
        "get", "workshop", "install", "build", "procurement",
        "lead", "governance", "check"
    ]

    if any(x in t for x in exclude_keywords):
        return False

    if any(x in t for x in include_keywords):
        return True

    return False


# -----------------------------
# NORMALISE NAME
# -----------------------------
def normalise(name: str) -> str:
    if not isinstance(name, str):
        return ""

    name = name.upper().strip()

    # remove codes like AMP8-FPS-XXXX
    name = re.sub(r"AMP8-[A-Z0-9\-]+", "", name)

    # remove multiple spaces
    name = re.sub(r"\s+", " ", name)

    return name.strip()


# -----------------------------
# EXTRACT DELIVERABLES
# -----------------------------
def extract_deliverables(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["is_deliverable"] = df["name"].apply(is_deliverable)
    df = df[df["is_deliverable"] == True]

    df["deliverable"] = df["name"].apply(normalise)

    return df[["deliverable", "finish"]]


# -----------------------------
# COMPARE SNAPSHOTS
# -----------------------------
def compare(cl31: pd.DataFrame, cl32: pd.DataFrame) -> pd.DataFrame:

    cl31 = extract_deliverables(cl31)
    cl32 = extract_deliverables(cl32)

    cl31 = cl31.rename(columns={"finish": "cl31_finish"})
    cl32 = cl32.rename(columns={"finish": "cl32_finish"})

    merged = pd.merge(cl31, cl32, on="deliverable", how="outer")

    # -------------------------
    # CHANGE TYPE LOGIC
    # -------------------------
    def classify(row):
        a = row.get("cl31_finish")
        b = row.get("cl32_finish")

        if pd.notna(a) and pd.notna(b):
            if a == b:
                return "UNCHANGED"
            elif b > a:
                return "DELAYED"
            else:
                return "ACCELERATED"

        if pd.notna(a) and pd.isna(b):
            return "REMOVED"

        if pd.isna(a) and pd.notna(b):
            return "NEW"

        return "UNKNOWN"

    merged["change_type"] = merged.apply(classify, axis=1)

    # -------------------------
    # DELTA DAYS
    # -------------------------
    merged["delta_days"] = (
        pd.to_datetime(merged["cl32_finish"], errors="coerce")
        - pd.to_datetime(merged["cl31_finish"], errors="coerce")
    ).dt.days

    # -------------------------
    # COMMENTS
    # -------------------------
    def comment(row):
        if row["change_type"] == "DELAYED":
            return "Shifted later vs CL31 baseline"
        if row["change_type"] == "NEW":
            return "Added scope in CL32"
        if row["change_type"] == "REMOVED":
            return "Dropped from CL32"
        if row["change_type"] == "UNCHANGED":
            return "Stable"
        if row["change_type"] == "ACCELERATED":
            return "Pulled earlier vs baseline"
        return ""

    merged["status_comment"] = merged.apply(comment, axis=1)

    return merged