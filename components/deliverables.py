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

    return "🟢 On Track"


# ---------------------------------------------------
# FORMAT DATE
# ---------------------------------------------------

def format_date(value):

    if pd.isna(value):
        return "-"

    return pd.to_datetime(value).strftime("%d-%b-%y")


# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------

def clean_text(value):

    if pd.isna(value):
        return ""

    return str(value).strip().lower()


# ---------------------------------------------------
# MAIN CARD
# ---------------------------------------------------

def build_deliverables_card(cl31, cl32):

    # ---------------------------------------------------
    # CARD STYLE
    # ---------------------------------------------------

    st.markdown("""
    <style>

    .deliverable-card {
        background-color: #111827;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #2d3748;
        margin-top: 15px;
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
    # CLEAN ACTIVITY NAMES
    # ---------------------------------------------------

    cl31["activity_clean"] = (
        cl31["Activity Name"]
        .astype(str)
        .apply(clean_text)
    )

    cl32["activity_clean"] = (
        cl32["Activity Name"]
        .astype(str)
        .apply(clean_text)
    )

    # ---------------------------------------------------
    # MERGE DIRECTLY USING ACTIVITY NAME
    # ---------------------------------------------------

    merged = pd.merge(

        cl31[
            [
                "activity_clean",
                "Activity Name",
                "Finish"
            ]
        ],

        cl32[
            [
                "activity_clean",
                "Activity Name",
                "Finish",
                "Total Float"
            ]
        ],

        on="activity_clean",
        how="inner",
        suffixes=("_CL31", "_CL32")
    )

    # ---------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------

    merged = merged.drop_duplicates(
        subset=["activity_clean"]
    )

    # ---------------------------------------------------
    # BUILD OUTPUT
    # ---------------------------------------------------

    rows = []

    for _, row in merged.iterrows():

        finish31 = row["Finish_CL31"]
        finish32 = row["Finish_CL32"]

        float_change = row.get(
            "Total Float",
            0
        )

        # -----------------------------------------------
        # DELTA
        # -----------------------------------------------

        if pd.notna(finish31) and pd.notna(finish32):

            delta = (
                pd.to_datetime(finish32)
                - pd.to_datetime(finish31)
            ).days

        else:
            delta = 0

        # -----------------------------------------------
        # STATUS
        # -----------------------------------------------

        status = status_logic(
            delta,
            float_change
        )

        # -----------------------------------------------
        # APPEND
        # -----------------------------------------------

        rows.append({

            "Deliverable":
            row["Activity Name_CL32"],

            "CL31 Finish":
            format_date(finish31),

            "CL32 Finish":
            format_date(finish32),

            "Δ Finish (Days)":
            f"{delta:+}",

            "Float Change":
            int(float_change),

            "Status":
            status
        })

    # ---------------------------------------------------
    # OUTPUT DF
    # ---------------------------------------------------

    out = pd.DataFrame(rows)

    # ---------------------------------------------------
    # SORT
    # ---------------------------------------------------

    if len(out) > 0:

        out = out.sort_values(
            by="Deliverable"
        )

    # ---------------------------------------------------
    # TABLE
    # ---------------------------------------------------

    st.dataframe(
        out,
        use_container_width=True,
        hide_index=True,
        height=700
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )