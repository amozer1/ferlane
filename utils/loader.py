import pandas as pd

def load_cl31(path="CL31.xlsx"):
    df = pd.read_excel(path)
    df = df.rename(columns={
        "Finish": "CL31 Finish",
        "Total Float": "CL31 Float"
    })
    return df


def load_cl32(path="CL32.xlsx"):
    df = pd.read_excel(path)
    df = df.rename(columns={
        "Finish": "CL32 Finish",
        "Total Float": "CL32 Float"
    })
    return df