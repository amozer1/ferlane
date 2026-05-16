import streamlit as st
import pandas as pd

from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables_table


st.set_page_config(layout="wide")

st.title("CL31 vs CL32 Deliverable Comparison")


@st.cache_data
def load_data():
    df31 = pd.read_excel("data/CL31.xlsx")
    df32 = pd.read_excel("data/CL32.xlsx")
    return df31, df32


df31, df32 = load_data()

comparison_df = prepare_comparison_df(df31, df32)

render_deliverables_table(comparison_df)