import streamlit as st

from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW
    # =========================
    col1, col2 = st.columns([1, 1])

    # =========================
    # LEFT CARD
    # =========================
    with col1:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📊 Programme Health
            </div>
        """, unsafe_allow_html=True)

        render_pie(result)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # RIGHT CARD
    # =========================
    with col2:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📈 Programme KPIs
            </div>
        """, unsafe_allow_html=True)

        kpi1, kpi2 = st.columns(2)
        kpi3, kpi4 = st.columns(2)

        kpi1.metric("Total", len(result))
        kpi2.metric("NEW", (result["Change Type"] == "NEW").sum())

        kpi3.metric("Delayed", (result["Change Type"] == "DELAYED").sum())
        kpi4.metric("Early", (result["Change Type"] == "EARLY").sum())

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # BOTTOM TABLE CARD
    # =========================
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">
            📋 Deliverable Register
        </div>
    """, unsafe_allow_html=True)

    render_table(result)

    st.markdown("</div>", unsafe_allow_html=True)