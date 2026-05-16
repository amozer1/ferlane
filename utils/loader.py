import pandas as pd
import re

DATA_PATH = "data"


def clean_deliverable(name):
    if pd.isna(name):
        return None

    name = str(name)

    # remove codes like AMP8-FPS-XXXX
    name = re.sub(r"AMP8-[A-Z0-9\-]+", "", name)

    # remove multiple spaces
    name = re.sub(r"\s+", " ", name)

    return name.strip()


def load_cl31():
    df = pd.read_excel(f"{DATA_PATH}/CL31-February.xlsx")

    df = df.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": "CL31 Finish"
    })

    df["Deliverable"] = df["Deliverable"].apply(clean_deliverable)
    df["CL31 Finish"] = pd.to_datetime(df["CL31 Finish"], errors="coerce")

    return df[["Deliverable", "CL31 Finish"]]


def load_cl32():
    df = pd.read_excel(f"{DATA_PATH}/CL32-May.xlsx")

    df = df.rename(columns={
        "Activity Name": "Deliverable",
        "Finish": "CL32 Finish"
    })

    df["Deliverable"] = df["Deliverable"].apply(clean_deliverable)
    df["CL32 Finish"] = pd.to_datetime(df["CL32 Finish"], errors="coerce")

    return df[["Deliverable", "CL32 Finish"]]