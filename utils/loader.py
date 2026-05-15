import pandas as pd


def load_data():

    df31 = pd.read_excel("data/CL31.xlsx")
    df32 = pd.read_excel("data/CL32.xlsx")

    return df31, df32