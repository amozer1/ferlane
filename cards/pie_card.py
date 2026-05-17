import streamlit as st
import plotly.graph_objects as go
import pandas as pd


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


def classify(row, today):

    if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
        return "On Track"

    if row["Finish"] < today and row["Activity % Complete"] < 100:
        return "Delayed"

    if row["Finish"] > today and row["Activity % Complete"] > 0:
        return "Accelerated"

    return "On Track"


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

    fig = go.Figure(
        data=[go.Pie(
            labels=summary.index,
            values=summary.values,
            sort=False,
            textinfo="label+percent",
            marker=dict(colors=[colors[k] for k in summary.index]),
            textfont=dict(color="black", size=14),
            pull=[0.02, 0.02, 0.02]
        )]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    # =========================
    # PURE STREAMLIT CARD FIX
    # =========================

    st.markdown(
        """
        <style>
        .block-card {
            background: white;
            border-radius: 18px;
            padding: 16px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        }

        .kpi-title {
            font-size: 18px;
            font-weight: 700;
            color: black;
            margin-bottom: 10px;
        }

        .legend-item {
            font-size: 15px;
            margin-bottom: 14px;
            color: black;
            display: flex;
            align-items: center;
        }

        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # TRUE CARD STRUCTURE (NO HTML WRAPPER)
    with st.container():

        col_card = st.columns(1)[0]

        with col_card:

            st.markdown('<div class="block-card">', unsafe_allow_html=True)

            st.markdown('<div class="kpi-title">Programme Status</div>', unsafe_allow_html=True)

            col1, col2 = st.columns([2.2, 1])

            with col1:
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

            with col2:
                st.markdown(f"""
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
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)