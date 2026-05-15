import pandas as pd
import streamlit as st


def status_logic(delta, float_change):
    if delta > 20 and float_change <= -10:
        return "🔴 Critical"
    elif delta > 15:
        return "🔴 Delayed"
    elif float_change < 0:
        return "🟡 At Risk"
    else:
        return "🟢 On Track"


def build_deliverables_card(cl31, cl32):

    st.markdown("### 📦 Deliverables Summary")

    # Merge by Activity Name (deliverable level)
    df = pd.merge(
        cl31[["Activity Name", "Finish"]],
        cl32[["Activity Name", "Finish", "Total Float"]],
        on="Activity Name",
        how="outer",
        suffixes=("_CL31", "_CL32")
    )

    df = df.dropna(subset=["Activity Name"])

    rows = []

    for _, r in df.iterrows():

        cl31_finish = r.get("Finish_CL31")
        cl32_finish = r.get("Finish_CL32")
        float_change = r.get("Total Float", 0)

        if pd.notna(cl31_finish) and pd.notna(cl32_finish):
            delta = (pd.to_datetime(cl32_finish) - pd.to_datetime(cl31_finish)).days
        else:
            delta = 0

        status = status_logic(delta, float_change)

        rows.append({
            "Deliverable": r["Activity Name"],
            "CL31 Finish": cl31_finish,
            "CL32 Finish": cl32_finish,
            "Δ Finish (Days)": f"{delta:+}",
            "Float Change": float_change,
            "Status": status
        })

    out = pd.DataFrame(rows)

    # ---- CARD UI ----
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