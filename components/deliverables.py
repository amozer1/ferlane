import streamlit as st


def render_deliverables(df):

    st.subheader("Deliverables Comparison")

    def highlight(row):

        colour = ""

        if row["Change Type"] == "DELAYED":
            colour = "#ffcccc"

        elif row["Change Type"] == "ACCELERATED":
            colour = "#d9ead3"

        elif row["Change Type"] == "NEW":
            colour = "#d0e0ff"

        elif row["Change Type"] == "REMOVED":
            colour = "#eeeeee"

        return [f"background-color: {colour}"] * len(row)

    styled = df.style.apply(highlight, axis=1)

    st.dataframe(
        styled,
        use_container_width=True,
        height=900
    )