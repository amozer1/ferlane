import pandas as pd
import streamlit as st


def status_logic(delta, float_change):
    if pd.isna(delta):
        return "⚪ No Data"

    if delta > 20 and float_change <= -10:
        return "🔴 Critical"
    elif delta > 15:
        return "🔴 Delayed"
    elif float_change < 0:
        return "🟡 At Risk"
    else:
        return "🟢 On Track"


def build_deliverables_card(df: pd.DataFrame):

    st.markdown("## 📦 Deliverables Dashboard")

    rows = []

    for _, r in df.iterrows():

        cl31 = r.get("cl31_finish")
        cl32 = r.get("cl32_finish")
        flt = r.get("float", 0)

        if pd.notna(cl31) and pd.notna(cl32):
            delta = (pd.to_datetime(cl32) - pd.to_datetime(cl31)).days
        else:
            delta = None

        rows.append({
            "Deliverable": r["activity"],
            "CL31 Finish": cl31,
            "CL32 Finish": cl32,
            "Δ Finish (Days)": delta,
            "Float Change": flt,
            "Status": status_logic(delta, flt)
        })

    out = pd.DataFrame(rows)

    # ---- STYLING CARD ----
    st.markdown("""
    <style>
    .deliverable-card {
        background: #0e1117;
        border: 1px solid #262730;
        padding: 16px;
        border-radius: 14px;
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