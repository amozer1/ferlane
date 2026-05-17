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

    # Clean percentage
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
# STATUS CLASSIFICATION
# =========================
def classify(row, today):

    if pd.isna(row["Start"]) or pd.isna(row["Finish"]):
        return "On Track"

    if (
        row["Finish"] < today
        and row["Activity % Complete"] < 100
    ):
        return "Delayed"

    if (
        row["Finish"] > today
        and row["Activity % Complete"] > 0
    ):
        return "Accelerated"

    return "On Track"


# =========================
# PIE CARD
# =========================
def render_pie(df):

    df = prepare(df)

    today = pd.Timestamp.today()

    # Create status column
    df["Status"] = df.apply(
        lambda r: classify(r, today),
        axis=1
    )

    # Status summary
    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    on_track = summary["On Track"]
    delayed = summary["Delayed"]
    accelerated = summary["Accelerated"]

    # =========================
    # CARD STYLE
    # =========================
    st.markdown(
        """
        <style>

        .pie-card {
            background: white;
            border-radius: 20px;
            padding: 15px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
            margin-bottom: 15px;
        }

        .indicator-row {
            display: flex;
            justify-content: space-around;
            margin-bottom: 10px;
            gap: 10px;
        }

        .indicator-box {
            flex: 1;
            border-radius: 14px;
            padding: 12px;
            text-align: center;
            font-weight: 600;
        }

        .indicator-title {
            font-size: 13px;
            color: black;
            margin-bottom: 5px;
        }

        .indicator-value {
            font-size: 24px;
            font-weight: 800;
            color: black;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # =========================
    # START CARD
    # =========================
    st.markdown(
        f"""
        <div class="pie-card">

            <div class="indicator-row">

                <div class="indicator-box" style="background:#FFF4B2;">
                    <div class="indicator-title">
                        On Track
                    </div>
                    <div class="indicator-value">
                        {on_track}
                    </div>
                </div>

                <div class="indicator-box" style="background:#FFD6D6;">
                    <div class="indicator-title">
                        Delayed
                    </div>
                    <div class="indicator-value">
                        {delayed}
                    </div>
                </div>

                <div class="indicator-box" style="background:#D8F5D0;">
                    <div class="indicator-title">
                        Accelerated
                    </div>
                    <div class="indicator-value">
                        {accelerated}
                    </div>
                </div>

            </div>
        """,
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

                hole=0.35,

                sort=False,

                textinfo="label+percent",

                marker=dict(
                    colors=[
                        "#FFD700",  # Yellow
                        "#FF3B30",  # Red
                        "#00C853"   # Green
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

        height=350,

        margin=dict(
            t=0,
            b=0,
            l=0,
            r=0
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
            y=-0.1,
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

    # =========================
    # END CARD
    # =========================
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )