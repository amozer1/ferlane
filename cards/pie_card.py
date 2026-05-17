import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# =========================
# DATA PREP
# =========================
def prepare(df):
    df = df.copy()
    df.columns = df.columns.astype(str).str.strip()

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
# CLASSIFY
# =========================
def classify(row, today):

    if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
        return "On Track"

    if row["Finish"] < today and row["Activity % Complete"] < 100:
        return "Delayed"

    if row["Finish"] > today and row["Activity % Complete"] > 0:
        return "Accelerated"

    return "On Track"


# =========================
# MAIN RENDER
# =========================
def render_pie(df):

    df = prepare(df)
    today = pd.Timestamp.today()

    df["Status"] = df.apply(lambda r: classify(r, today), axis=1)

    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    colors = {
        "On Track": "#FFD700",
        "Delayed": "#FF3B30",
        "Accelerated": "#00C853"
    }

    # =========================
    # PIE FIGURE
    # =========================
    fig = go.Figure(
        data=[go.Pie(
            labels=summary.index,
            values=summary.values,
            sort=False,
            textinfo="label+percent",
            marker=dict(colors=[colors[k] for k in summary.index]),
            textfont=dict(color="black", size=14),
            hole=0,
            pull=[0.02, 0.02, 0.02]
        )]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=380,
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False  # IMPORTANT (we build our own side legend)
    )

    # =========================
    # CARD LAYOUT (TALL + SIDE BY SIDE)
    # =========================
    st.markdown(
        """
        <style>
        .card {
            background: white;
            padding: 18px;
            border-radius: 18px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.10);
            height: 450px;
        }

        .label-box {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 14px;
            color: black;
        }

        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            font-size: 15px;
            color: black;
        }

        .dot {
            height: 12px;
            width: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="label-box">Programme Status</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with col2:
        st.markdown(
            f"""
            <div class="legend-item">
                <div class="dot" style="background:#FFD700;"></div>
                On Track: {summary['On Track']}
            </div>

            <div class="legend-item">
                <div class="dot" style="background:#FF3B30;"></div>
                Delayed: {summary['Delayed']}
            </div>

            <div class="legend-item">
                <div class="dot" style="background:#00C853;"></div>
                Accelerated: {summary['Accelerated']}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)