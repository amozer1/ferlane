import streamlit as st
import pandas as pd

from utils.loader import load_data
from utils.comparison import build_variance_table
from utils.classifications import classify_status

st.title("Executive Dashboard")

# Load data
cl31, cl32 = load_data()

# Build comparison dataset
df = build_variance_table(cl31, cl32)

# Apply status classification
df["Status"] = df.apply(classify_status, axis=1)

# Format table
display_df = df[[
    "Deliverable",
    "CL31 Finish",
    "CL32 Finish",
    "Delta_Days",
    "Float_Change",
    "Status"
]].copy()

# Rename for UI
display_df.columns = [
    "Deliverable",
    "CL31 Finish",
    "CL32 Finish",
    "Δ Finish (Days)",
    "Float Change",
    "Status"
]

# --------------------------
# CARD 1 UI
# --------------------------
st.subheader("Delivery Variance Summary (CL31 vs CL32)")

st.dataframe(
    display_df.style.applymap(
        lambda x: "color:red;" if x == "Critical"
        else "color:orange;" if x == "At Risk"
        else "color:green;" if x == "On Track"
        else ""
    ),
    use_container_width=True
)