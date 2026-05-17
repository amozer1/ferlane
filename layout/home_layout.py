import streamlit as st

from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW (2 CARDS)
    # =========================
    top1, top2 = st.columns(2)

    # =========================
    # PIE CARD
    # =========================
    with top1:

        st.markdown("""
        <div class="dashboard-card" style="height:360px;">
            <div class="card-title">
                📊 Key Programme Updates
            </div>
        """, unsafe_allow_html=True)

        render_pie(result)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # SUMMARY CARD
    # =========================
    with top2:

        st.markdown("""
        <div class="dashboard-card" style="height:360px;">
            <div class="card-title">
                📌 Programme Summary
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="font-size:15px; line-height:1.6;">

        • CL31 baseline compared against CL32 forecast dates.<br><br>

        • Delayed = activities pushed later than baseline.<br><br>

        • Accelerated = activities brought forward.<br><br>

        • On Track = no change in programme dates.<br><br>

        • Deliverables listed in programme order.

        </div>
        """, unsafe_allow_html=True)

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