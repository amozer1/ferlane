import streamlit as st
import pandas as pd


def render_cl32_card(cl31: pd.DataFrame, cl32: pd.DataFrame):
    """
    Clean NEC-style Deliverable Movement Card (CL31 vs CL32)
    """

    st.subheader("Deliverable Movement (CL31 vs CL32)")

    df = cl32.copy()

    # -------------------------------------------------
    # 1. STANDARDISE COLUMN NAMES
    # -------------------------------------------------
    rename_map = {
        "Total Float": "Float Change",
        "Float": "Float Change",
        "CL31 Finish Date": "CL31 Finish",
        "CL32 Finish Date": "CL32 Finish"
    }

    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    # -------------------------------------------------
    # 2. ENSURE CORE COLUMNS EXIST
    # -------------------------------------------------
    required_cols = [
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Float Change",
        "Status"
    ]

    if "Deliverable" not in df.columns:
        df["Deliverable"] = df.index.astype(str)

    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    # -------------------------------------------------
    # 3. FORMAT STATUS (NEC STYLE)
    # -------------------------------------------------
    def format_status(x):
        x = str(x).lower()

        if "critical" in x:
            return "🔴 Critical"
        elif "delayed" in x:
            return "🔴 Delayed"
        elif "risk" in x:
            return "🟡 At Risk"
        elif x in ["", "none", "nan"]:
            return ""
        else:
            return "🟢 On Track"

    df["Status"] = df["Status"].apply(format_status)

    # -------------------------------------------------
    # 4. FORMAT DELTA (ensure + sign)
    # -------------------------------------------------
    def format_delta(x):
        try:
            x = float(x)
            return f"{x:+.0f}"
        except:
            return ""

    if "Delta (Days)" in df.columns:
        df["Delta (Days)"] = df["Delta (Days)"].apply(format_delta)

    # -------------------------------------------------
    # 5. FINAL TABLE ORDER
    # -------------------------------------------------
    final_table = df[[
        "Deliverable",
        "CL31 Finish",
        "CL32 Finish",
        "Delta (Days)",
        "Float Change",
        "Status"
    ]]

    # -------------------------------------------------
    # 6. DISPLAY CARD
    # -------------------------------------------------
    st.dataframe(
        final_table,
        use_container_width=True,
        height=300
    )