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

    fig = go.Figure(
        data=[go.Pie(
            labels=summary.index,
            values=summary.values,
            sort=False,
            textinfo="label+percent",
            marker=dict(
                colors=["#FFD700", "#FF3B30", "#00C853"]
            ),
            textfont=dict(color="black", size=14),
            pull=[0.02, 0.02, 0.02]
        )]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=320,
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=True,
        legend=dict(
            orientation="h",
            y=-0.15,
            x=0.5,
            xanchor="center",
            font=dict(color="black")
        )
    )

    # =========================
    # STREAMLIT CARD (NO HTML)
    # =========================
    with st.container():
        st.markdown(
            """
            <style>
            div[data-testid="stContainer"] {
                background: white;
                padding: 12px;
                border-radius: 16px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.10);
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )