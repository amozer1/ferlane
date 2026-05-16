import streamlit as st


def render_deliverables_table(df):
    """
    Render CL31 vs CL32 deliverables comparison table
    """

    st.subheader("📦 Deliverables Comparison")

    # Clean display formatting
    display_df = df.copy()

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    # Optional summary metrics
    col1, col2, col3 = st.columns(3)

    total = len(df)
    delayed = len(df[df["Status / Comment"].str.contains("Delay|Slippage", na=False)])
    maintained = len(df[df["Status / Comment"] == "Maintained"])

    col1.metric("Total Deliverables", total)
    col2.metric("Delayed", delayed)
    col3.metric("Maintained", maintained)
