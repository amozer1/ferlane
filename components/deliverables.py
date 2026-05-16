import streamlit as st


def render_deliverables(df):

    st.subheader("CL31 vs CL32 Deliverables Comparison")

    if df.empty:
        st.warning("No data available. Please upload valid CL31 and CL32 files.")
        return

    # Colour rules
    def style_rows(row):
        if row["Change Type"] == "ACCELERATED":
            return ["background-color: #d4f7d4"] * len(row)
        elif row["Change Type"] == "DELAYED":
            return ["background-color: #ffd6d6"] * len(row)
        elif row["Change Type"] == "NEW":
            return ["background-color: #d6e4ff"] * len(row)
        elif row["Change Type"] == "REMOVED":
            return ["background-color: #e0e0e0"] * len(row)
        elif row["Change Type"] == "UNCHANGED":
            return ["background-color: #f5f5f5"] * len(row)
        return [""] * len(row)

    styled_df = df.style.apply(style_rows, axis=1)

    st.dataframe(styled_df, use_container_width=True)

    # Optional quick summary
    st.markdown("### Summary")

    summary = df["Change Type"].value_counts().reset_index()
    summary.columns = ["Change Type", "Count"]

    st.dataframe(summary, use_container_width=True)