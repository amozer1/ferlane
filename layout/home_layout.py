import streamlit as st

from cards.pie_card import render_pie
from cards.delay_cl32 import render_delayed_table
from cards.table_card import render_table


def render_home(result, df32):

    # =========================
    # GLOBAL PAGE LAYOUT FIX
    # =========================
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # =========================
    # TOP ROW (PIE + DELAYED)
    # =========================
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.container()
        st.subheader("📊 Schedule Summary (CL32)")
        render_pie(df32)

    with col2:
        st.container()
        st.subheader("🔴 Delayed Activities (CL32)")
        render_delayed_table(df32)

    # =========================
    # FULL WIDTH TABLE
    # =========================
    st.markdown("---")

    st.container()
    st.subheader("📋 Deliverable Register (CL31 vs CL32)")
    render_table(result)