import streamlit as st
import pandas as pd


def get_delayed(df):
    df = df.copy()

    df.columns = df.columns.astype(str).str.strip()

    # dates
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Finish"] = pd.to_datetime(df["Finish"], errors="coerce")

    # % complete cleanup
    df["Activity % Complete"] = (
        df["Activity % Complete"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    df["Activity % Complete"] = pd.to_numeric(df["Activity % Complete"], errors="coerce").fillna(0)

    today = pd.Timestamp.today()

    delayed = df[
        (df["Finish"] < today) &
        (df["Activity % Complete"] < 100)
    ].copy()

    delayed["Delay (Days)"] = (today - delayed["Finish"]).dt.days

    return delayed.sort_values("Delay (Days)", ascending=False)


def render_table(df):
    delayed = get_delayed(df)

    if delayed.empty:
        st.success("No delayed activities 🎯")
        return

    html = """
    <style>
        .delay-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            border-radius: 10px;
            overflow: hidden;
        }

        .delay-table thead {
            background: linear-gradient(90deg, #ff4b4b, #b5179e);
            color: white;
        }

        .delay-table th {
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }

        .delay-table td {
            padding: 10px;
            color: white;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }

        .delay-table tbody tr:nth-child(even) {
            background-color: rgba(255,255,255,0.03);
        }

        .delay-table tbody tr:hover {
            background-color: rgba(255,75,75,0.10);
        }

        .delay-badge {
            background: #ff4b4b;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            color: white;
            font-weight: 600;
        }
    </style>

    <table class="delay-table">
        <thead>
            <tr>
                <th>Activity ID</th>
                <th>Activity Name</th>
                <th>Start</th>
                <th>Finish</th>
                <th>Delay (Days)</th>
                <th>Comments</th>
            </tr>
        </thead>
        <tbody>
    """

    for _, row in delayed.iterrows():
        html += f"""
        <tr>
            <td>{row.get('Activity ID','')}</td>
            <td>{row.get('Activity Name','')}</td>
            <td>{row['Start'].date() if pd.notna(row['Start']) else ''}</td>
            <td>{row['Finish'].date() if pd.notna(row['Finish']) else ''}</td>
            <td><span class="delay-badge">{int(row['Delay (Days)'])}</span></td>
            <td>{row.get('Comments','')}</td>
        </tr>
        """

    html += """
        </tbody>
    </table>
    """

    st.markdown(html, unsafe_allow_html=True)