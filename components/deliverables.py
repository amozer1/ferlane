# =========================
# components/deliverables.py
# =========================

import pandas as pd
import streamlit as st


# ---------------------------------------------------
# STATUS LOGIC
# ---------------------------------------------------
def status_logic(delta, float_change):

    if delta >= 20 and float_change <= -10:
        return "🔴 Critical"

    elif delta >= 15:
        return "🔴 Delayed"

    elif float_change < 0:
        return "🟡 At Risk"

    else:
        return "🟢 On Track"


# ---------------------------------------------------
# FIND FINISH DATE
# ---------------------------------------------------
def get_finish(df, activity_name):

    row = df[df["Activity Name"] == activity_name]

    if len(row) == 0:
        return None

    return row.iloc[0]["Finish"]


# ---------------------------------------------------
# FIND FLOAT
# ---------------------------------------------------
def get_float(df, activity_name):

    row = df[df["Activity Name"] == activity_name]

    if len(row) == 0:
        return 0

    if "Total Float" not in row.columns:
        return 0

    value = row.iloc[0]["Total Float"]

    try:
        return float(value)
    except:
        return 0


# ---------------------------------------------------
# MAIN CARD
# ---------------------------------------------------
def build_deliverables_card(cl31, cl32):

    st.markdown("""
    <style>

    .deliverable-card {
        background-color: #111827;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #2d3748;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .card-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-bottom: 18px;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="deliverable-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📦 Deliverables Summary</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # DELIVERABLE MAPPING
    # ---------------------------------------------------
    deliverables = [

        {
            "name": "3D Modelling",
            "cl31": "3D Modelling",
            "cl32": "3D Modelling"
        },

        {
            "name": "Concept Shaft Design",
            "cl31": "Shaft design inc. benching, cover slab, pipe entry/exit",
            "cl32": "Concept Shaft Design"
        },

        {
            "name": "Scope Freeze",
            "cl31": "Submission of Outline Design Pack",
            "cl32": "Outline Design Scope Freeze (Minimum Requirements)"
        },

        {
            "name": "Outline Submission",
            "cl31": "Final Submission",
            "cl32": "Outline Design Submission"
        }
    ]

    rows = []

    # ---------------------------------------------------
    # BUILD ROWS
    # ---------------------------------------------------
    for item in deliverables:

        cl31_finish = get_finish(cl31, item["cl31"])
        cl32_finish = get_finish(cl32, item["cl32"])

        float_change = get_float(cl32, item["cl32"])

        # -------------------------
        # DELTA
        # -------------------------
        if pd.notna(cl31_finish) and pd.notna(cl32_finish):

            delta = (
                pd.to_datetime(cl32_finish)
                - pd.to_datetime(cl31_finish)
            ).days

        else:
            delta = 0

        # -------------------------
        # STATUS
        # -------------------------
        status = status_logic(delta, float_change)

        # -------------------------
        # FORMAT DATES
        # -------------------------
        if pd.notna(cl31_finish):
            cl31_finish = pd.to_datetime(cl31_finish).strftime("%d-%b-%y")
        else:
            cl31_finish = "-"

        if pd.notna(cl32_finish):
            cl32_finish = pd.to_datetime(cl32_finish).strftime("%d-%b-%y")
        else:
            cl32_finish = "-"

        rows.append({

            "Deliverable": item["name"],

            "CL31 Finish": cl31_finish,

            "CL32 Finish": cl32_finish,

            "Δ Finish (Days)": f"{delta:+}",

            "Float Change": int(float_change),

            "Status": status
        })

    # ---------------------------------------------------
    # DATAFRAME
    # ---------------------------------------------------
    out = pd.DataFrame(rows)

    st.dataframe(
        out,
        use_container_width=True,
        hide_index=True,
        height=260
    )

    st.markdown("</div>", unsafe_allow_html=True)