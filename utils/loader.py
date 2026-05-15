import pandas as pd

def load_data():
    cl31 = pd.read_excel("data/CL31.xlsx")
    cl32 = pd.read_excel("data/CL32.xlsx")

    return cl31, cl32