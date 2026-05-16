import streamlit as st
import pandas as pd

from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables_table

st.set_page_config(layout="wide")

st.title("CL31 vs CL32 Deliverables Comparison")


def load_file(path):
    return pd.read_excel(path)


# SAFE AUTO LOAD (Streamlit Cloud compatible)
df31 = load_file("data/CL31.xlsx")
df32 = load_file("data/CL32.xlsx")

comparison_df = prepare_comparison_df(df31, df32)

render_deliverables_table(comparison_df)