import streamlit as st
from utils.loader import load_schedule
from components.deliverables import build_deliverables_card

st.set_page_config(layout="wide")

st.title("Design Dashboard")

cl31, cl32 = load_schedule("CL31.xlsx", "CL32.xlsx")

build_deliverables_card(cl31, cl32)