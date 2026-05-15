import streamlit as st

with right:

    st.subheader("Total Float Distribution")

    hist = px.histogram(
        merged,
        x="total float_32",
        nbins=20,
        title="Float Distribution"
    )

    st.plotly_chart(hist, use_container_width=True)

# VARIANCE CHART
st.subheader("Variance to Baseline")

variance = merged.sort_values("finish_32")

line = px.line(
    variance,
    x="finish_32",
    y="delta_finish_days",
    title="CL31 vs CL32 Finish Variance"
)

st.plotly_chart(line, use_container_width=True)

# LOOK AHEAD
st.subheader("4 Week Look Ahead")

today = pd.Timestamp.today()
future = today + pd.Timedelta(days=28)

lookahead = merged[
    (merged["start_32"] >= today) &
    (merged["start_32"] <= future)
]

st.dataframe(
    lookahead[
        [
            "activity id",
            "activity name_32",
            "start_32",
            "finish_32",
            "total float_32",
            "status"
        ]
    ],
    use_container_width=True,
    height=300
)

# KEY DATA TABLE
st.subheader("Key Data Table")

summary = pd.DataFrame({
    "Metric": [
        "Total Activities",
        "Critical Activities",
        "Delayed Activities",
        "Accelerated Activities"
    ],
    "Value": [
        len(merged),
        critical,
        len(merged[merged["status"] == "Delayed"]),
        len(merged[merged["status"] == "Accelerated"])
    ]
})

st.table(summary)

# COMMENTARY
st.subheader("Executive Commentary")

st.info(
    f"Programme currently contains {critical} critical activities. "
    f"There are {len(merged[merged['status'] == 'Delayed'])} delayed activities "
    f"against the baseline programme."
)