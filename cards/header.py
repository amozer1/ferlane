import streamlit as st
import pandas as pd


def render_header():

    today = pd.Timestamp.today().strftime("%d %b %Y")

    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #d8f3dc, #b7e4c7);
        padding: 18px 22px;
        border-radius: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
        border: 1px solid #95d5b2;
    ">

        <div style="
            font-size: 26px;
            font-weight: 800;
            color: #1b4332;
            letter-spacing: 1px;
        ">
            FL DM PROGRAMME DASHBOARD
        </div>

        <div style="
            margin-top: 6px;
            font-size: 14px;
            color: #2d6a4f;
            font-weight: 500;
        ">
            📅 Report Date: {today}
        </div>

    </div>
    """, unsafe_allow_html=True)