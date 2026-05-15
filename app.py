import streamlit as st

st.title("Debug Mode")

st.write("App started successfully")

try:
    from utils.cleaner import clean_programme
    st.success("cleaner imported")
except Exception as e:
    st.error("cleaner FAILED")
    st.exception(e)

try:
    from utils.comparison import compare_programmes
    st.success("comparison imported")
except Exception as e:
    st.error("comparison FAILED")
    st.exception(e)

try:
    from utils.calculations import calculate_deltas
    st.success("calculations imported")
except Exception as e:
    st.error("calculations FAILED")
    st.exception(e)

try:
    from utils.classifications import classify_activity
    st.success("classifications imported")
except Exception as e:
    st.error("classifications FAILED")
    st.exception(e)