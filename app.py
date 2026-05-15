import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_programme_data
from utils.classifications import classify_float
from utils.analytics import compute_kpis
from core.commentary_engine import generate_commentary

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="FERLANE NEC Controls", layout="wide")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}

.block-container {
    padding: 1rem 2rem 2rem 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
cl31, cl32 = load_programme_data()
cl32 = classify_float(cl32)
kpis = compute_kpis(cl32)
commentary = generate_commentary(cl31, cl32, kpis)

# -----------------------------
# HEADER
# -----------------------------
st.title("FERLANE NEC Programme Controls Dashboard")
st.caption("CL31 vs CL32 | NEC Clause 31/32 | Programme Intelligence Layer")

st.divider()

# =====================================================
# ROW 1 — KPI + FLOAT DISTRIBUTION (SPLIT PANEL)
# =====================================================
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Programme KPIs")

    a, b = st.columns(2)
    a.metric("Total", kpis["total"])
    b.metric("Avg Float", f"{kpis['avg_float']:.1f}")

    c, d = st.columns(2)
    c.metric("Critical", kpis["critical"])
    d.metric("Near Crit", kpis["near_critical"])

    st.metric("Non Critical", kpis["non_critical"])

with col2:
    st.subheader("Float Distribution")

    fig_float = px.histogram(cl32, x="Float", nbins=25)
    st.plotly_chart(fig_float, use_container_width=True)

st.divider()

# =====================================================
# ROW 2 — STATUS + VARIANCE
# =====================================================
col3, col4 = st.columns(2)

with col3:
    st.subheader("Activity Status Split")

    status = cl32["Status"].value_counts().reset_index()
    status.columns = ["Status", "Count"]

    fig_status = px.pie(status, names="Status", values="Count")
    st.plotly_chart(fig_status, use_container_width=True)

with col4:
    st.subheader("Baseline Variance (CL31 vs CL32)")

    fig_var = go.Figure()

    if "Finish" in cl31.columns and "Finish" in cl32.columns:
        fig_var.add_trace(go.Scatter(y=cl31["Finish"], name="CL31"))
        fig_var.add_trace(go.Scatter(y=cl32["Finish"], name="CL32"))

    st.plotly_chart(fig_var, use_container_width=True)

st.divider()

# =====================================================
# ROW 3 — CRITICAL + LOOKAHEAD TABLE (FULL WIDTH SPLIT)
# =====================================================
col5, col6 = st.columns(2)

with col5:
    st.subheader("Critical Path Activities")

    critical = cl32[cl32["Status"] == "Critical"]

    st.dataframe(critical, height=400, use_container_width=True)

with col6:
    st.subheader("Lookahead (Top Risk Activities)")

    lookahead = cl32.sort_values("Float").head(15)

    st.dataframe(lookahead, height=400, use_container_width=True)

st.divider()

# =====================================================
# ROW 4 — NEC COMMENTARY (FULL WIDTH)
# =====================================================
st.subheader("NEC Programme Commentary (Clause 31 / 32)")

st.info(commentary)

st.divider()

# =====================================================
# ROW 5 — EXPORT PANEL
# =====================================================
st.subheader("Export Controls")

st.download_button(
    "Download CL32 Programme Data",
    cl32.to_csv(index=False),
    file_name="FERLANE_CL32.csv"
)