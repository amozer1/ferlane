import streamlit as st
import plotly.graph_objects as go
import pandas as pd


# =========================
# PREPARE DATA
# =========================
def prepare(df):
    df = df.copy()

    # Clean column names
    df.columns = df.columns.astype(str).str.strip()

    # Convert dates
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # Clean % Complete
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
    if row["Finish"] < today and row["Activity % Complete"] < 100:
        return "Delayed"

    # Accelerated / active ahead of finish
    if row["Finish"] > today and row["Activity % Complete"] > 0:
        return "Accelerated"

    # Default
    return "On Track"


# =========================
# RENDER PIE CHART
# =========================
def render_pie(df):

    df = prepare(df)

    today = pd.Timestamp.today()

    # Create status column
    df["Status"] = df.apply(
        lambda r: classify(r, today),
        axis=1
    )

    # Summary counts
    summary = df["Status"].value_counts().reindex(
        ["On Track", "Delayed", "Accelerated"],
        fill_value=0
    )

    # Pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=summary.index,
                values=summary.values,
                hole=0,
                sort=False,
                textinfo="label+percent",

                marker=dict(
                    colors=[
                        "#FFD700",  # On Track = Yellow
                        "#FF0000",  # Delayed = Red
                        "#00C853"   # Accelerated = Green
                    ]
                )
            )
        ]
    )

    fig.update_layout(
        title="Programme Status Overview",
        height=350,
        margin=dict(t=50, b=10, l=10, r=10),
        showlegend=True,

        paper_bgcolor="#140021",
        plot_bgcolor="#140021",

        font=dict(
            color="white",
            size=13
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# DEMO / TEST
# =========================
if __name__ == "__main__":

    st.set_page_config(layout="wide")

    st.title("Programme Dashboard")

    # Sample test data
    data = {
        "Start": [
            "2026-01-01",
            "2026-02-01",
            "2026-03-01",
            "2026-04-01"
        ],

        "Finish": [
            "2026-05-01",
            "2026-04-01",
            "2026-12-01",
            "2026-10-01"
        ],

        "Activity % Complete": [
            "100%",
            "40%",
            "50%",
            "0%"
        ]
    }

    df = pd.DataFrame(data)

    render_pie(df)