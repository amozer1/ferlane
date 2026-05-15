import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_programme_data
from utils.classifications import classify_float
from utils.analytics import compute_kpis
from core.commentary_engine import generate_commentary

# -----------------------------
# PAGE CONFIG (EXECUTIVE STYLE)
# -----------------------------
st.set_page_config(
    page_title="FERLANE NEC Controls",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
section[data-testid="stSidebar"] {display: none;}
.block-container {padding-top: 1rem; padding-left: 2rem; padding-right: 2rem;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA PIPELINE
# -----------------------------
cl31, cl32 = load_programme_data()
cl32 = classify_float(cl32)
kpis = compute_kpis(cl32)
commentary = generate_commentary(cl31, cl32, kpis)

# -----------------------------
# HEADER
# -----------------------------
st.title("FERLANE NEC Programme Controls Dashboard")
st.caption("CL31 vs CL32 | NEC Clause 31 / 32 | Float & Variance Analytics")

st.divider()

# -----------------------------
# KPI STRIP
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Activities", kpis["total"])
col2.metric("Critical", kpis["critical"])
col3.metric("Near Critical", kpis["near_critical"])
col4.metric("Non Critical", kpis["non_critical"])
col5.metric("Avg Float", f"{kpis['avg_float']:.1f} days")

st.divider()

# -----------------------------
# SCHEDULE HEALTH (CL32)
# -----------------------------
st.subheader("Schedule Health Overview (CL32)")

status_counts = cl32["Status"].value_counts().reset_index()
status_counts.columns = ["Status", "Count"]

fig1 = px.bar(
    status_counts,
    x="Status",
    y="Count",
    text="Count"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# -----------------------------
# FLOAT DISTRIBUTION
# -----------------------------
st.subheader("Float Distribution")

fig2 = px.histogram(
    cl32,
    x="Float",
    nbins=20
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# -----------------------------
# BASELINE VARIANCE (CL31 vs CL32)
# -----------------------------
st.subheader("Baseline Variance (CL31 vs CL32)")

fig3 = go.Figure()

if "Finish" in cl31.columns and "Finish" in cl32.columns:
    fig3.add_trace(go.Scatter(
        y=cl31["Finish"],
        name="CL31 Baseline",
        line=dict(width=3)
    ))

    fig3.add_trace(go.Scatter(
        y=cl32["Finish"],
        name="CL32 Current",
        line=dict(width=3)
    ))

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# -----------------------------
# CRITICAL ACTIVITIES
# -----------------------------
st.subheader("Critical Activities Register")

critical_df = cl32[cl32["Status"] == "Critical"]

st.dataframe(
    critical_df,
    use_container_width=True,
    height=300
)

st.divider()

# -----------------------------
# LOOKAHEAD (TOP RISKS)
# -----------------------------
st.subheader("Lookahead Window (Top Risk Activities)")

lookahead = cl32.sort_values("Float").head(15)

st.dataframe(
    lookahead,
    use_container_width=True,
    height=350
)

st.divider()

# -----------------------------
# NEC COMMENTARY ENGINE
# -----------------------------
st.subheader("NEC Programme Commentary (Clause 31 / 32 Insight)")

st.info(commentary)

st.divider()

# -----------------------------
# EXPORT
# -----------------------------
st.subheader("Export Programme Data")

st.download_button(
    "Download CL32 Programme",
    cl32.to_csv(index=False),
    file_name="FERLANE_CL32_export.csv",
    mime="text/csv"
)