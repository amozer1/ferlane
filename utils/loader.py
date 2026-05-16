import pandas as pd
import re


def load_excel(path: str):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df


def is_deliverable_row(row):
    name = str(row.get("Activity Name", "")).strip()

    if name == "" or name.lower() == "nan":
        return False

    # reject pure structural rows
    reject = [
        "design", "procurement", "construction",
        "milestones", "key dates", "programme",
        "deliverables"
    ]

    if name.lower() in reject:
        return False

    # reject rows that are just timing containers (no meaning)
    if len(name) < 5:
        return False

    # must have some scheduling info
    if pd.isna(row.get("Finish")) and pd.isna(row.get("Start")):
        return False

    return True


def clean_date(value):
    if pd.isna(value):
        return pd.NaT

    value = str(value)
    value = re.sub(r"[A\*]", "", value).strip()

    return pd.to_datetime(value, errors="coerce")