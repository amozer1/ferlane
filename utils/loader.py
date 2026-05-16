import pandas as pd

DATA_PATH = "data"

def load_cl31():
    df = pd.read_excel(f"{DATA_PATH}/CL31-February.xlsx")

    df = df.rename(columns={
        "Activity Name": "Activity",
        "Finish": "Finish"
    })

    df = df[["Activity", "Finish"]].copy()
    df["Activity"] = df["Activity"].astype(str).str.strip()
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    return df


def load_cl32():
    df = pd.read_excel(f"{DATA_PATH}/CL32-May.xlsx")

    df = df.rename(columns={
        "Activity Name": "Activity",
        "Finish": "Finish"
    })

    df = df[["Activity", "Finish"]].copy()
    df["Activity"] = df["Activity"].astype(str).str.strip()
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    return df