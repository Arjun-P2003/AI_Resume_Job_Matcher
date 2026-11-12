
import streamlit as st
from modules.dashboard import show_dashboard

st.set_page_config(
    page_title="Dashboard Test",
    layout="wide"
)

st.title("Actual Dashboard Module Test")

test_results = {
    "matched_skills": [
        "Python", "SQL", "Machine Learning",
        "Pandas", "NumPy", "FastAPI"
    ],
    "missing_skills": ["Docker", "AWS", "TensorFlow"],
    "extra_skills": ["Java", "HTML", "CSS"],
    "match_percentage": 66.67
}

show_dashboard(test_results, 72.50)
