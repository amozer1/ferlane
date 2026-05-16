import streamlit as st
from cards.pie_card import render_pie
from cards.table_card import render_table


def render_home(result):

    # =========================
    # TOP ROW (2 CARDS)
    # =========================
    col1, col2 = st.columns(2)

    # =========================
    # CARD 1 - PIE
    # =========================
    with col1:
        st.markdown("### 📊 Programme Health")

        st.markdown(
            """
            <div style="
                background-color:#240046;
                padding:20px;
                border-radius:15px;
                box-shadow:0px 4px 12px rgba(0,0,0,0.4);
            ">
            """,
            unsafe_allow_html=True
        )

        render_pie(result)

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # CARD 2 - KPIs
    # =========================
    with col2:
        st.markdown("### 📈 Summary KPIs")

        st.markdown(
            """
            <div style="
                background-color:#240046;
                padding:20px;
                border-radius:15px;
                box-shadow:0px 4px 12px rgba(0,0,0,0.4);
            ">
            """,
            unsafe_allow_html=True
        )

        colA, colB = st.columns(2)
        colA.metric("Total", len(result))
        colB.metric("NEW", (result["Change Type"] == "NEW").sum())

        colC, colD = st.columns(2)
        colC.metric("Delayed", (result["Change Type"] == "DELAYED").sum())
        colD.metric("Early", (result["Change Type"] == "EARLY").sum())

        st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # BOTTOM CARD (TABLE)
    # =========================
    st.markdown("---")

    st.markdown("### 📋 Deliverable Register")

    st.markdown(
        """
        <div style="
            background-color:#240046;
            padding:20px;
            border-radius:15px;
            box-shadow:0px 4px 12px rgba(0,0,0,0.4);
        ">
        """,
        unsafe_allow_html=True
    )

    render_table(result)

    st.markdown("</div>", unsafe_allow_html=True)