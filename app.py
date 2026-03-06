"""
Fitness Tracker - Streamlit Web Application
Interactive web interface for the fitness tracker.
"""

import streamlit as st

# Page configuration
st.set_page_config(
  page_title="Fitness Tracker",
  page_icon="💪",
  layout="wide",
  initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
  .metric-card {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
  }
  .stProgress > div > div > div > div {
    background-color: #ff4b4b;
  }
</style>
""", unsafe_allow_html=True)