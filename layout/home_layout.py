import streamlit as st

from cards.pie_card import render_pie
from cards.delay_card import render_delayed_table
from cards.table_card import render_table


def render_home(result, df32):

    # =========================
    # TOP ROW
    # =========================
    col1, col2 = st.columns([1, 1])

    # =========================
    # PIE (CL32 ONLY)
    # =========================
    with col1:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                📊 Schedule Summary (CL32)
            </div>
        """, unsafe_allow_html=True)

        render_pie(df32)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # DELAYED TABLE (CL32 ONLY)
    # =========================
    with col2:
        st.markdown("""
        <div class="dashboard-card">
            <div class="card-title">
                🔴 Delayed Deliverables (CL32)
            </div>
        """, unsafe_allow_html=True)

        render_delayed_table(df32)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # DELIVERABLE REGISTER (CL31 vs CL32)
    # =========================
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">
            📋 Deliverable Register (CL31 vs CL32)
        </div>
    """, unsafe_allow_html=True)

    render_table(result)

    st.markdown("</div>", unsafe_allow_html=True)