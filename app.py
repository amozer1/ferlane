import streamlit as st

from data.loader import load_schedule
from components.deliverables import build_deliverables_card


CL31_PATH = "data/CL31.xlsx"
CL32_PATH = "data/CL32.xlsx"


st.set_page_config(page_title="Deliverables Dashboard", layout="wide")

st.title("📊 Programme Dashboard")


df = load_schedule(CL31_PATH, CL32_PATH)

build_deliverables_card(df)