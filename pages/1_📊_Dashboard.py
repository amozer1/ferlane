import streamlit as st
import pandas as pd
import plotly.express as px

from utils.cleaner import clean_primavera
from utils.comparison import merge_programmes
from utils.calculations import calculate_deltas
from utils.classifications import apply_classification

# LOAD
df31 = pd.read_excel("data/CL31.xlsx")
df32 = pd.read_excel("data/CL32.xlsx")

# CLEAN
df31 = clean_primavera(df31)
df32 = clean_primavera(df32)

# MERGE
df = merge_programmes(df31, df32)

# CALCULATE
df = calculate_deltas(df)

# CLASSIFY
df = apply_classification(df)

# KPI
st.title("📊 NEC Dashboard")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Activities", len(df))
k2.metric("Delayed", len(df[df["status"] == "Delayed"]))
k3.metric("Accelerated", len(df[df["status"] == "Accelerated"]))
k4.metric("Critical", len(df[df["critical"] == "Critical"]))

# PIE
pie = df["status"].value_counts().reset_index()
pie.columns = ["Status", "Count"]

fig = px.pie(
    pie,
    names="Status",
    values="Count",
    color="Status",
    color_discrete_map={
        "Delayed": "red",
        "Accelerated": "green",
        "On Track": "yellow"
    }
)

st.plotly_chart(fig, use_container_width=True)

# TABLE
st.dataframe(df, use_container_width=True)