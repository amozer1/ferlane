import streamlit as st

from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW
    # =========================
    col1, col2 = st.columns([1, 1])

    # =========================
    # PIE CARD
    # =========================
    with col1:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📊 Programme Update
            </div>
        """, unsafe_allow_html=True)

        render_pie(result)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # SECOND CARD
    # =========================
    with col2:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📌 Key Programme Summary
            </div>
        """, unsafe_allow_html=True)

        delayed = (result["Change Type"] == "DELAYED").sum()
        early = (result["Change Type"] == "EARLY").sum()
        unchanged = (result["Change Type"] == "UNCHANGED").sum()

        st.metric("Delayed", delayed)
        st.metric("Accelerated", early)
        st.metric("On Track", unchanged)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # TABLE CARD
    # =========================
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">
            📋 Deliverable Register
        </div>
    """, unsafe_allow_html=True)

    render_table(result)

    st.markdown("</div>", unsafe_allow_html=True)