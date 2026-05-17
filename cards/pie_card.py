import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# =========================
# CLEAN + NORMALISE DATA
# =========================
def prepare(df):
    df = df.copy()

    # clean column names just in case
    df.columns = df.columns.astype(str).str.strip()

    # safe datetime conversion
    if "Start" in df.columns:
        df["Start"] = pd.to_datetime(df["Start"], errors="coerce")

    if "Finish" in df.columns:
        df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # clean % complete
    if "Activity % Complete" in df.columns:
        df["Activity % Complete"] = (
            df["Activity % Complete"]
            .astype(str)
            .str.replace("%", "", regex=False)
        )
        df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce").fillna(0)
    else:
        df["Activity % Complete"] = 0

    return df


# =========================
# CLASSIFICATION LOGIC
# =========================
def classify(row, today):
    start = row.get("Start")
    finish = row.get("Finish")
    pct = row.get("Activity % Complete", 0)

    # missing dates → default safe category
    if pd.isna(start) or pd.isna(finish):
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
            sort=False,
            hole=0,
            showlegend=False   # ✅ REMOVE PLOTLY LEGEND COMPLETELY
        )]
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=5, b=5, l=5, r=5),
        height=320,
        showlegend=False  # ✅ extra safety
    )

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Status Overview")

        st.markdown(f"🟡 On Track: {summary['On Track']}")
        st.markdown(f"🔴 Delayed: {summary['Delayed']}")
        st.markdown(f"🟢 Accelerated: {summary['Accelerated']}")