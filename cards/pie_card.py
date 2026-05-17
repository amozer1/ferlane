import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# =========================
# PREPARE DATA
# =========================
def prepare(df):

    df = df.copy()

    # Clean columns
    df.columns = df.columns.astype(str).str.strip()

    # Convert dates
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # Clean % complete
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
# CLASSIFY STATUS
# =========================
def classify(row, today):

    # Missing dates
    if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
        return "On Track"

    # Delayed
    if (
        row["Finish"] < today
        and row["Activity % Complete"] < 100
    ):
        return "Delayed"

    # Accelerated
    if (
        row["Finish"] > today
        and row["Activity % Complete"] > 0
    ):
        return "Accelerated"

    return "On Track"


# =========================
# PIE CHART
# =========================
def render_pie(df):

    df = prepare(df)

    today = pd.Timestamp.today()

    # Apply classification
    df["Status"] = df.apply(
        lambda r: classify(r, today),
        axis=1
    )

    # Count statuses
    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    # =========================
    # CARD STYLE
    # =========================
    st.markdown(
        """
        <style>

        .pie-card {
            background-color: white;
            padding: 8px;
            border-radius: 18px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
            margin-bottom: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="pie-card">',
        unsafe_allow_html=True
    )

    # =========================
    # PIE CHART
    # =========================
    fig = go.Figure(
        data=[
            go.Pie(
                labels=summary.index,
                values=summary.values,

                sort=False,

                textinfo="label+percent",

                marker=dict(
                    colors=[
                        "#FFD700",  # On Track = Yellow
                        "#FF3B30",  # Delayed = Red
                        "#00C853"   # Accelerated = Green
                    ]
                ),

                textfont=dict(
                    size=14,
                    color="black"
                ),

                pull=[0.02, 0.02, 0.02]
            )
        ]
    )

    fig.update_layout(

        height=340,

        margin=dict(
            t=0,
            b=10,
            l=10,
            r=10
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            color="black",
            size=14
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(
                color="black",
                size=13
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )