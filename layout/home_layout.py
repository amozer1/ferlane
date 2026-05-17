import streamlit as st

from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW
    # =========================
    col1, col2 = st.columns(2)

    # =========================
    # PIE CARD
    # =========================
    with col1:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">📊 Key Programme Updates</div>
        </div>
        """, unsafe_allow_html=True)

        render_pie(result)

    # =========================
    # SUMMARY CARD
    # =========================
    with col2:

        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">📌 Programme Summary</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("""
        • CL31 baseline compared against CL32 forecast dates  
        • Delayed = later than baseline  
        • Accelerated = earlier than baseline  
        • On Track = unchanged  
        """)

    # =========================
    # TABLE
    # =========================
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">📋 Deliverable Register</div>
        </div>
    """, unsafe_allow_html=True)

    render_table(result)