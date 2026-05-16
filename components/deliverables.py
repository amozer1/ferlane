import streamlit as st


def style_table(df):
    def color(row):
        if row["Change Type"] == "DELAYED":
            return ["background-color:#ffcccc"] * len(row)
        if row["Change Type"] == "MODIFIED":
            return ["background-color:#fff2cc"] * len(row)
        if row["Change Type"] == "NEW":
            return ["background-color:#d9fdd3"] * len(row)
        if row["Change Type"] == "REMOVED":
            return ["background-color:#e6e6e6"] * len(row)
        return [""] * len(row)

    return df.style.apply(color, axis=1)


def render_deliverables(df):
    st.subheader("Deliverables Comparison (CL31 vs CL32)")

    st.dataframe(
        style_table(df),
        use_container_width=True
    )