import streamlit as st

st.set_page_config(
    page_title="FERLANE NEC Control System",
    layout="wide"
)

st.title("⚖️ FERLANE NEC Programme Control System")

st.markdown("""
### Welcome

This system compares:
- Clause 31 (Baseline Programme)
- Clause 32 (Updated Programme)

Navigate using the left sidebar:
- 📊 Dashboard
- 📋 Activity Details
- 📈 Analytics
- 📤 Exports
""")

st.info("Use sidebar to begin NEC programme analysis.")