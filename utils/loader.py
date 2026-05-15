import pandas as pd


def load_cl31(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    df = df.rename(columns={
        "Activity Name": "activity",
        "Finish": "cl31_finish"
    })
    return df[["activity", "cl31_finish"]]


def load_cl32(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    df = df.rename(columns={
        "Activity Name": "activity",
        "Finish": "cl32_finish",
        "Total Float": "float"
    })
    return df[["activity", "cl32_finish", "float"]]


def load_schedule(cl31_path: str, cl32_path: str):
    cl31 = load_cl31(cl31_path)
    cl32 = load_cl32(cl32_path)

    df = pd.merge(cl31, cl32, on="activity", how="outer")

    return df