import streamlit as st

from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW
    # =========================
    col1, col2 = st.columns([1, 1])

    # =========================
    # LEFT CARD (PIE)
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
    # RIGHT CARD (EMPTY FOR NOW)
    # =========================
    with col2:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📌 Upcoming Dashboard Section
            </div>
        """, unsafe_allow_html=True)

        st.info("Reserved for milestone tracker, float analysis or variance trends.")

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