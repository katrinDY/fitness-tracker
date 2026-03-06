"""
Fitness Tracker - Streamlit Web Application
Interactive web interface for the fitness tracker.
"""

import streamlit as st
from models.workout_tracker import WorkoutTracker

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

# Initialize session state
if 'tracker' not in st.session_state:
  st.session_state.tracker = WorkoutTracker("streamlit_fitness_data.json")

tracker = st.session_state.tracker

def dashboard_page():
  """Dashboard page showing workout summary and analytics."""

def add_workout_page():
  """Page for adding new workouts."""

def workout_history_page():
  """Page showing workout history with filtering options."""

def goals_page():
  """Page for setting and tracking fitness goals."""

def analytics_page():
  """Page showing analytics and visualizations of workout data."""

def setup_user_profile():
  """User profile setup and update."""

def main():
  """Main application"""
  
  # Sidebar
  with st.sidebar:
    st.title("Fitness Tracker")
    
    if tracker.user:
      st.success(f"👋 {tracker.user.first_name} {tracker.user.last_name}")
      st.caption(f"BMI: {tracker.user.calculate_bmi()} ({tracker.user.get_bmi_category()})")
    else:
      st.warning("⚠️ No profile set up")
    
    st.divider()
    
    page = st.radio(
      "Navigation",
      ["Dashboard", "Add Workout", "Workout History", "Goals", "Analytics", "Profile"],
      label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick stats
    if tracker.workouts:
      st.subheader("📊 Quick Stats")
      st.metric("Total Workouts", len(tracker.workouts))
      st.metric("Total Duration (min)", sum(w.duration for w in tracker.workouts))
      st.metric("Total Calories Burned", sum(w.calories_burned for w in tracker.workouts))

  # Main content
  if page == "Dashboard":
    dashboard_page()
  elif page == "Add Workout":
    add_workout_page()
  elif page == "Workout History":
    workout_history_page()
  elif page == "Goals":
    goals_page()
  elif page == "Analytics":
    analytics_page()
  elif page == "Profile":
    setup_user_profile()

if __name__ == "__main__":
  main()
