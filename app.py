import streamlit as st

from utils.loader import load_programmes
from components.deliverables import build_deliverables

st.set_page_config(page_title="CL31 vs CL32 Dashboard", layout="wide")

st.title("Programme Deliverables Comparison (CL31 vs CL32)")

CL31_FILE = "data/CL31-February.xlsx"
CL32_FILE = "data/CL32-May.xlsx"

df31 = load_programmes(CL31_FILE)
df32 = load_programmes(CL32_FILE)

deliverables_df = build_deliverables(df31, df32)

deliverables_df = deliverables_df[
    [
        "Activity Name",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Change Type",
        "Status / Comment"
    ]
]

st.subheader("Deliverables Comparison Table")
st.dataframe(deliverables_df, use_container_width=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliverables", len(deliverables_df))
col2.metric("Delayed", (deliverables_df["Change Type"] == "DELAYED").sum())
col3.metric("New", (deliverables_df["Change Type"] == "NEW").sum())
col4.metric("Removed", (deliverables_df["Change Type"] == "REMOVED").sum())