import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_pie(df):

    # =========================
    # TITLE
    # =========================
    st.markdown("### Schedule Summary (CL32)")

    df = df.copy()

    # =========================
    # CLEAN DATA
    # =========================
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce")

    today = pd.to_datetime("today")

    # =========================
    # TIME PROGRESS
    # =========================
    duration = (df["Finish"] - df["Start"]).dt.days
    elapsed = (today - df["Start"]).dt.days

    time_progress = (elapsed / duration) * 100

    # =========================
    # CLASSIFICATION LOGIC
    # =========================
    df["Status"] = "On Track"

    df.loc[df["Activity % Complete"] < (time_progress - 5), "Status"] = "Delayed"
    df.loc[df["Activity % Complete"] > (time_progress + 5), "Status"] = "Accelerated"

    # =========================
    # COUNTS
    # =========================
    counts = df["Status"].value_counts()

    on_track = counts.get("On Track", 0)
    delayed = counts.get("Delayed", 0)
    accelerated = counts.get("Accelerated", 0)

    # =========================
    # PIE DATA (NO ZERO DISPLAY)
    # =========================
    labels = []
    values = []
    colors = []

    if on_track > 0:
        labels.append("On Track")
        values.append(on_track)
        colors.append("gold")

    if delayed > 0:
        labels.append("Delayed")
        values.append(delayed)
        colors.append("red")

    if accelerated > 0:
        labels.append("Accelerated")
        values.append(accelerated)
        colors.append("green")

    # =========================
    # PIE CHART (LOCKED FIT)
    # =========================
    col1, col2 = st.columns([1.2, 1])

    with col1:

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors),
                    textinfo="label+value+percent",
                    sort=False
                )
            ]
        )

        fig.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="white",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.markdown("### Key Status")

        st.markdown(f"""
        🟡 **On Track:** {on_track}  
        🔴 **Delayed:** {delayed}  
        🟢 **Accelerated:** {accelerated}
        """)