import streamlit as st
import matplotlib.pyplot as plt


def render_pie(result):

    counts = result["Change Type"].value_counts()

    labels = ["DELAYED", "EARLY", "NEW", "UNCHANGED"]

    values = [
        counts.get("DELAYED", 0),
        counts.get("EARLY", 0),
        counts.get("NEW", 0),
        counts.get("UNCHANGED", 0)
    ]

    colors = ["red", "green", "gold", "lightgray"]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct="%1.0f%%", colors=colors)
    ax.set_title("Programme Health Overview")

    st.subheader("Programme Status (Pie Chart)")
    st.pyplot(fig)