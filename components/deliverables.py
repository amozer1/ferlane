import streamlit as st
import pandas as pd


def render_table(df: pd.DataFrame):

    st.subheader("📊 CL31 vs CL32 Deliverable Comparison")

    # styling
    def highlight(row):
        if row["Change Type"] == "NEW":
            return ["background-color:#d4edda"] * len(row)
        elif row["Change Type"] == "REMOVED":
            return ["background-color:#f8d7da"] * len(row)
        elif row["Change Type"] == "MODIFIED":
            return ["background-color:#fff3cd"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df.style.apply(highlight, axis=1),
        use_container_width=True,
        hide_index=True
    )


def render_summary(df):

    st.subheader("📌 Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", len(df))
    col2.metric("New", len(df[df["Change Type"] == "NEW"]))
    col3.metric("Removed", len(df[df["Change Type"] == "REMOVED"]))
    col4.metric("Modified", len(df[df["Change Type"] == "MODIFIED"]))