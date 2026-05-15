import streamlit as st

from views.executive import render_executive
from views.comparison import render_comparison
from views.critical import render_critical
from views.analytics import render_analytics
from views.exports import render_exports

st.set_page_config(
    page_title="FERLANE NEC Programme Controls",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit chrome completely
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}
.block-container {padding-top: 1.2rem;}
</style>
""", unsafe_allow_html=True)

# Simple top navigation (no sidebar system)
tabs = st.tabs([
    "Executive",
    "Schedule Comparison",
    "Critical Path",
    "Analytics",
    "Exports"
])

with tabs[0]:
    render_executive()

with tabs[1]:
    render_comparison()

with tabs[2]:
    render_critical()

with tabs[3]:
    render_analytics()

with tabs[4]:
    render_exports()