import streamlit as st

st.set_page_config(
    page_title="FERLANE NEC Dashboard",
    layout="wide"
)

with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.markdown(
    """
    <h1 style='text-align:center;color:#002b5c;'>
    🏗️ FERLANE NEC Dashboard
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='text-align:center;margin-bottom:40px;'>
    Enterprise NEC Programme Controls Platform
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:

    st.markdown("""
    <div class='card'>
    <h2>📊 Executive Dashboard</h2>
    <p>Programme KPIs and NEC reporting</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Executive Dashboard"):
        st.switch_page("views/executive.py")

with c2:

    st.markdown("""
    <div class='card'>
    <h2>📋 Programme Comparison</h2>
    <p>Clause 31 vs Clause 32 comparison</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Programme Comparison"):
        st.switch_page("views/comparison.py")

with c3:

    st.markdown("""
    <div class='card'>
    <h2>⚠️ Critical Path Analysis</h2>
    <p>Float and critical path analysis</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Critical Analysis"):
        st.switch_page("views/critical.py")

with c4:

    st.markdown("""
    <div class='card'>
    <h2>📈 Trend Analytics</h2>
    <p>Programme trends and float erosion</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Trend Analytics"):
        st.switch_page("views/analytics.py")