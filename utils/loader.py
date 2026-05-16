import pandas as pd


def load_schedule():

    cl31 = pd.read_excel("data/CL31.xlsx")
    cl32 = pd.read_excel("data/CL32.xlsx")

    cl31.columns = cl31.columns.str.strip()
    cl32.columns = cl32.columns.str.strip()

    return cl31, cl32