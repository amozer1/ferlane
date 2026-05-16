import streamlit as st

from utils.loader import load_schedule
from components.deliverables import build_deliverables_card


cl31, cl32 = load_schedule()

build_deliverables_card(cl31, cl32)