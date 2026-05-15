import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FOLDER = Path("data")

@st.cache_data(show_spinner=True)
def load_all_files():

    files = list(DATA_FOLDER.glob("*.xlsx"))

    if len(files) == 0:
        st.error("No Excel files found in /data")
        st.stop()

    df_list = []

    for file in files:

        df = pd.read_excel(file, engine="openpyxl")

        # 🔥 ABSOLUTE GUARANTEE COLUMN EXISTS
        df.insert(0, "Source File", str(file.name))

        # 🔥 DEBUG CHECK (TEMPORARY)
        if "Source File" not in df.columns:
            st.error(f"'Source File' NOT CREATED for {file.name}")
            st.stop()

        df_list.append(df)

    combined = pd.concat(df_list, ignore_index=True)

    # FINAL SAFETY CHECK
    if "Source File" not in combined.columns:
        st.error("CRITICAL: Source File missing after concat")
        st.stop()

    return combined