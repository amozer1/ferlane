import pandas as pd
import streamlit as st


# -----------------------------
# STATUS ENGINE
# -----------------------------
def status_logic(delta, float_change):
    if delta > 20 and float_change <= -10:
        return "🔴 Critical"
    elif delta > 15:
        return "🔴 Delayed"
    elif float_change < 0:
        return "🟡 At Risk"
    else:
        return "🟢 On Track"


# -----------------------------
# FILTER ONLY TOP-LEVEL DELIVERABLES
# -----------------------------
def get_deliverables(df):
    df = df.copy()

    # Keep only summary / deliverable-level rows
    df = df[
        df["Activity ID"].isna()
        | ~df["Activity ID"].astype(str).str.contains("FER-", na=False)
    ]

    return df


# -----------------------------
# MAIN CARD
# -----------------------------
def build_deliverables_card(cl31, cl32):

    st.markdown("### 📦 Deliverables Summary")

    # Clean datasets
    cl31 = get_deliverables(cl31)
    cl32 = get_deliverables(cl32)

    # Merge CL31 vs CL32
    df = pd.merge(
        cl31[["Activity Name", "Finish"]],
        cl32[["Activity Name", "Finish", "Total Float"]],
        on="Activity Name",
        how="inner",
        suffixes=("_CL31", "_CL32")
    )

    rows = []

    for _, r in df.iterrows():

        cl31_finish = pd.to_datetime(r["Finish_CL31"], errors="coerce")
        cl32_finish = pd.to_datetime(r["Finish_CL32"], errors="coerce")

        float_change = r.get("Total Float", 0)

        # Delta calculation
        if pd.notna(cl31_finish) and pd.notna(cl32_finish):
            delta = (cl32_finish - cl31_finish).days
        else:
            delta = 0

        status = status_logic(delta, float_change)

        rows.append({
            "Deliverable": r["Activity Name"],
            "CL31 Finish": cl31_finish.date() if pd.notna(cl31_finish) else None,
            "CL32 Finish": cl32_finish.date() if pd.notna(cl32_finish) else None,
            "Δ Finish (Days)": f"{delta:+}",
            "Float Change": float_change,
            "Status": status
        })

    out = pd.DataFrame(rows)

    # -----------------------------
    # CARD UI STYLING
    # -----------------------------
    st.markdown("""
        <style>
        .deliverable-card {
            background-color: #0e1117;
            padding: 18px;
            border-radius: 14px;
            border: 1px solid #262730;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="deliverable-card">', unsafe_allow_html=True)

    st.dataframe(
        out,
        use_container_width=True,
        hide_index=True
    )

    st.markdown('</div>', unsafe_allow_html=True)