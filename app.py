import streamlit as st

from utils.loader import load_programme
from utils.deliverables import compare_deliverables


st.set_page_config(
    page_title="CL31 vs CL32 Deliverables",
    layout="wide"
)

CL31_FILE = "data/CL31.xlsx"
CL32_FILE = "data/CL32.xlsx"

cl31 = load_programme(CL31_FILE)
cl32 = load_programme(CL32_FILE)

comparison = compare_deliverables(cl31, cl32)

st.title("Deliverables Comparison")

st.markdown("### CL31 vs CL32")

st.dataframe(
    comparison,
    use_container_width=True,
    hide_index=True
)