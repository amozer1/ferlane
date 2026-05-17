import streamlit as st


def render_table(result):

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True,
        height=350
    )