import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# =========================
# PREP DATA
# =========================
def prepare(df):
    df = df.copy()

    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["Activity % Complete"] = pd.to_numeric(
        df["Activity % Complete"],
        errors="coerce"
    ).fillna(0)

    return df


# =========================
# CLASSIFICATION LOGIC
# =========================
def classify(row, today):
    finish = row["Finish"]
    pct = row["Activity % Complete"]

    if pd.isna(finish):
        return "On Track"

    # 🔴 DELAYED
    if finish < today and pct < 100:
        return "Delayed"

    # 🟢 ACCELERATED
    if finish > today and pct > 0:
        return "Accelerated"

    # 🟡 ON TRACK
    return "On Track"


# =========================
# PIE RENDER
# =========================
def render_pie(df):
    df = prepare(df)
    today = pd.Timestamp.today()

    df["Status"] = df.apply(lambda r: classify(r, today), axis=1)

    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    labels = ["On Track", "Delayed", "Accelerated"]
    values = [
        summary["On Track"],
        summary["Delayed"],
        summary["Accelerated"]
    ]

    colors = ["#FFD700", "#FF4B4B", "#00C853"]

    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            textinfo="label+percent",
            hole=0,
            sort=False
        )]
    )

    # =========================
    # IMPORTANT FIX (FIT INSIDE CARD)
    # =========================
    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        showlegend=False,   # remove Plotly legend completely
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    # Make pie stay inside canvas
    fig.update_traces(
        textposition="inside",
        insidetextorientation="radial"
    )

    # =========================
    # CARD WRAPPER
    # =========================
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-title">Schedule Summary</div>
    """, unsafe_allow_html=True)

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    # =========================
    # CUSTOM LEGEND (ONLY ONE)
    # =========================
    st.markdown("""
    <div style="display:flex; justify-content:space-around; margin-top:8px; font-size:14px;">
        <div>🟡 On Track</div>
        <div>🔴 Delayed</div>
        <div>🟢 Accelerated</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)