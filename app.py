import streamlit as st
from utils.loader import prepare_comparison_df
from components.deliverables import render_deliverables

st.set_page_config(page_title="Deliverables Dashboard", layout="wide")

st.title("Programme Deliverables Dashboard (CL31 vs CL32)")

st.markdown("Upload CL31 and CL32 programme files to generate comparison.")

# Uploads (fixes ALL file path issues)
cl31_file = st.file_uploader("Upload CL31 File", type=["xlsx"])
cl32_file = st.file_uploader("Upload CL32 File", type=["xlsx"])

if cl31_file and cl32_file:

    df = prepare_comparison_df(cl31_file, cl32_file)

    render_deliverables(df)

elif cl31_file or cl32_file:
    st.info("Please upload BOTH CL31 and CL32 files.")

else:
    st.warning("Waiting for file uploads...")