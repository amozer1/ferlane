import streamlit as st

from cards.pie_card import render_pie
from cards.delay_cl32 import render_delayed_table
from cards.table_card import render_table


def render_home(result, df32):

    col1, col2 = st.columns(2)

    with col1:
        st.container(border=True)
        st.subheader("📊 Schedule Summary (CL32)")
        render_pie(df32)

    with col2:
        st.container(border=True)
        st.subheader("🔴 Delayed Activities (CL32)")
        render_delayed_table(df32)

    st.container(border=True)
    st.subheader("📋 Deliverable Register (CL31 vs CL32)")
    render_table(result)