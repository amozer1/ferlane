import streamlit as st
import pandas as pd


def render_formatted_table(df):
    df = df.copy()

    # =========================
    # DISPLAY FORMATTING ONLY
    # =========================
    df["Start"] = pd.to_datetime(df["Start"]).dt.strftime("%d-%b-%Y")
    df["Finish"] = pd.to_datetime(df["Finish"]).dt.strftime("%d-%b-%Y")

    # =========================
    # COLOUR LOGIC (NO DATA CHANGE)
    # =========================
    def colour_delay(val):
        try:
            v = float(val)
            if v >= 50:
                return "background-color:#5a0000; color:white; font-weight:bold"   # Critical (dark red)
            elif v >= 30:
                return "background-color:#8b1e1e; color:white; font-weight:bold"   # High
            elif v >= 15:
                return "background-color:#a66a00; color:white; font-weight:bold"   # Medium
            else:
                return "background-color:#4a4a00; color:white; font-weight:bold"   # Low
        except:
            return ""

    styled = df.style

    # =========================
    # HEADER + TABLE STYLE
    # =========================
    styled = styled.set_table_styles([
        {
            "selector": "th",
            "props": [
                ("background-color", "#2b3a55"),
                ("color", "white"),
                ("font-size", "13px"),
                ("font-weight", "600"),
                ("text-transform", "uppercase"),
                ("letter-spacing", "1px"),
                ("padding", "10px"),
                ("border-bottom", "2px solid #4da3ff"),
                ("text-align", "left")
            ]
        },
        {
            "selector": "td",
            "props": [
                ("padding", "8px"),
                ("background-color", "#1c2233"),
                ("color", "#f1f1f1"),
                ("border-bottom", "1px solid #2a3347"),
                ("border-right", "1px solid #2a3347"),
                ("vertical-align", "top")
            ]
        },
        {
            "selector": "table",
            "props": [
                ("border-collapse", "collapse"),
                ("width", "100%"),
                ("background-color", "#1c2233")
            ]
        }
    ])

    # =========================
    # APPLY COLOUR TO DELAY COLUMN ONLY
    # =========================
    styled = styled.applymap(colour_delay, subset=["Delay (Days)"])

    st.write(styled)