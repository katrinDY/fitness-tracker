"""
Fitness Tracker - Streamlit Web Application
Interactive web interface for the fitness tracker.
"""

from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from models.workout_tracker import WorkoutTracker
from models.user import User
from models.workout import Workout

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

TOTAL_WORKOUTS = "Total Workouts"

def dashboard_page():
  """Dashboard page showing workout summary and analytics."""
  st.header("📊 Dashboard")
  
  if not tracker.workouts:
    st.info("No data yet. Add some workouts to see your progress!")
    return
  
  # Overall statistics
  stats = tracker.get_total_stats()
  
  col1, col2, col3, col4, col5 = st.columns(5)
  
  with col1:
    st.metric(TOTAL_WORKOUTS, stats['total_workouts'])
  with col2:
    st.metric("Total Duration", f"{stats['total_duration']} min")
  with col3:
    st.metric("Total Calories", f"{stats['total_calories']:,}")
  with col4:
    st.metric("Avg Duration", f"{stats['avg_duration']:.1f} min")
  with col5:
    st.metric("Current Streak", f"{stats['current_streak']} 🔥")
  
  st.divider()
  
  # Charts
  col1, col2 = st.columns(2)
  
  with col1:
    st.subheader("📈 Calories Over Time")
  
    # Prepare data for line chart
    workout_dates = [w.date.strftime("%Y-%m-%d") for w in tracker.workouts]
    workout_calories = [w.calories_burned for w in tracker.workouts]
    
    fig = px.line(
      x=workout_dates,
      y=workout_calories,
      labels={'x': 'Date', 'y': 'Calories Burned'},
      markers=True
    )
    
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)
  
  with col2:
    st.subheader("🥧 Workout Types Distribution")
    
    # Count workout types
    workout_counts = {}
    for w in tracker.workouts:
      workout_counts[w.workout_type.capitalize()] = workout_counts.get(w.workout_type.capitalize(), 0) + 1
    
    fig = px.pie(
      names=list(workout_counts.keys()),
      values=list(workout_counts.values()),
      hole=0.4
    )
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
  
  # Weekly breakdown
  st.divider()
  st.subheader("📅 This Week's Activity")
  
  weekly = tracker.get_weekly_summary()
  
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("Workouts This Week", weekly['workout_count'])
  with col2:
    st.metric("Duration This Week", f"{weekly['total_duration']} min")
  with col3:
    st.metric("Calories This Week", f"{weekly['total_calories']:,}")
  
  # Daily breakdown
  today = datetime.now()
  week_start = today - timedelta(days=today.weekday())
  
  daily_data = []
  for i in range(7):
    day = week_start + timedelta(days=i)
    day_workouts = [w for w in tracker.workouts if w.date.date() == day.date()]
    
    daily_data.append({
      "Day": day.strftime("%a"),
      "Workouts": len(day_workouts),
      "Duration": sum(w.duration for w in day_workouts),
      "Calories": sum(w.calories_burned for w in day_workouts)
    })
  
  df = pd.DataFrame(daily_data)
  
  fig = go.Figure()
  fig.add_trace(go.Bar(x=df['Day'], y=df['Calories'], name='Calories'))
  fig.update_layout(
    title="Daily Calorie Burn This Week",
    xaxis_title="Day",
    yaxis_title="Calories",
    height=300
  )
  st.plotly_chart(fig, use_container_width=True)

def add_workout_page():
  """Page for adding new workouts."""
  st.header("💪 Add New Workout")
  
  if not tracker.user:
    st.warning("⚠️ Please set up your user profile first!")
    return
  
  with st.form("add_workout_form"):
    col1, col2 = st.columns(2)
    
    with col1:
      workout_type = st.selectbox(
        "Workout Type",
        options=list(Workout.CALORIE_RATES.keys()),
        format_func=lambda x: x.capitalize()
      )
      duration = st.number_input("Duration (minutes)", min_value=1, max_value=300, value=30)
      notes = st.text_area("Notes (optional)", placeholder="How did you feel? Any observations?")
      
    with col2:
      workout_date = st.date_input("Workout Date", value=datetime.now())
      workout_time = st.time_input("Workout Time", value=datetime.now().time())
    
    submitted = st.form_submit_button("➕ Add Workout")
    
    if submitted:
      workout_datetime = datetime.combine(workout_date, workout_time)
      workout = Workout(workout_type, duration, workout_datetime, notes, tracker.user.weight)
      tracker.add_workout(workout)
      st.success(f"✅ Workout added! You burned {workout.calories_burned} calories! 🔥")
      
      # Check for goal completion
      for goal in tracker.goals:
        if goal.completed and goal.completed_at and \
          (datetime.now() - goal.completed_at).total_seconds() < 5:
          st.balloons()
          st.success(f"🎉 Goal achieved: {goal.description}!"
          )
      st.rerun()


def workout_history_page():
  """Page showing workout history with filtering options."""
  st.header("📅 Workout History")
  
  if not tracker.workouts:
    st.info("No workouts logged yet. Start by adding a workout!")
    return

  # Filter options
  col1, col2, col3 = st.columns(3)
  
  with col1:
    filter_type = st.selectbox(
      "Filter by type",
      ["All"] + list(set(w.workout_type for w in tracker.workouts)),
    )
  
  with col2:
    date_range = st.selectbox(
      "Date Range",
      ["All Time", "This Week", "This Month", "Last 7 Days", "Last 30 Days"]
    )
  
  with col3:
    sort_by = st.selectbox(
      "Sort by",
      ["Date (newest)", "Date (oldest)", "Calories", "Duration (longest)"]
    )

  # Apply filters
  filtered_workouts = tracker.workouts.copy()
  
  if filter_type != "All":
    filtered_workouts = [w for w in filtered_workouts if w.workout_type == filter_type]
    
  if date_range == "This Week":
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    filtered_workouts = tracker.get_workouts_by_date_range(week_start, today)
  elif date_range == "This Month":
    today = datetime.now()
    month_start = today.replace(day=1)
    filtered_workouts = tracker.get_workouts_by_date_range(month_start, today)
  elif date_range == "Last 7 Days":
    today = datetime.now()
    last_week = today - timedelta(days=7)
    filtered_workouts = tracker.get_workouts_by_date_range(last_week, today)
  elif date_range == "Last 30 Days":
    today = datetime.now()
    last_month = today - timedelta(days=30)
    filtered_workouts = tracker.get_workouts_by_date_range(last_month, today)
  
  # Sort
  if sort_by == "Date (Newest)":
    filtered_workouts.sort(key=lambda w: w.date, reverse=True)
  elif sort_by == "Date (Oldest)":
    filtered_workouts.sort(key=lambda w: w.date)
  elif sort_by == "Calories":
    filtered_workouts.sort(key=lambda w: w.calories_burned, reverse=True)
  elif sort_by == "Duration":
    filtered_workouts.sort(key=lambda w: w.duration, reverse=True)
    
  # Display summary
  st.divider()
  col1, col2, col3, col4 = st.columns(4)
  
  total_duration = sum(w.duration for w in filtered_workouts)
  total_calories = sum(w.calories_burned for w in filtered_workouts)
  
  with col1:
    st.metric(TOTAL_WORKOUTS, len(filtered_workouts))
  with col2:
    st.metric("Total Duration", f"{total_duration} min")
  with col3:
    st.metric("Total Calories", f"{total_calories:,} cal")
  with col4:
    avg_duration = total_duration / len(filtered_workouts) if filtered_workouts else 0
    st.metric("Avg Duration", f"{avg_duration:.1f} min")
    
  # Display workouts
  st.divider()
  
  if not filtered_workouts:
    st.info("No workouts match your filters.")
    return

  # Create DataFrame for display
  workout_data = []
  for w in filtered_workouts:
    workout_data.append({
      "Date": w.date.strftime("%Y-%m-%d"),
      "Time": w.date.strftime("%H:%M"),
      "Type": w.workout_type.capitalize(),
      "Duration (min)": w.duration,
      "Calories": w.calories_burned,
      "Intensity": w.get_intensity(),
      "Notes": w.notes[:50] + "..." if len(w.notes) > 50 else w.notes
    })
  
  df = pd.DataFrame(workout_data)
  st.dataframe(df, use_container_width=True, hide_index=True)

def goals_page():
  """Page for setting and tracking fitness goals."""

def analytics_page():
  """Page showing analytics and visualizations of workout data."""

def setup_user_profile():
  """User profile setup and update."""
  st.header("👤 User Profile")
  
  with st.form("user_profile_form"):
    col1, col2 = st.columns(2)
    
    with col1:
      first_name = st.text_input("First Name", value=tracker.user.first_name if tracker.user else "")
      age = st.number_input("Age", min_value=25, max_value=120, value=tracker.user.age if tracker.user else 25)
      gender = st.selectbox("Gender", ["male", "female"], index=0 if not tracker.user else (0 if tracker.user.gender == "male" else 1))

    with col2:
      last_name = st.text_input("Last Name", value=tracker.user.last_name if tracker.user else "")
      height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=float(tracker.user.height) if tracker.user else 170.0, step=0.1)
      weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=float(tracker.user.weight) if tracker.user else 70.0, step=0.1)
  
    submitted = st.form_submit_button("💾 Save Profile")
  
    if submitted:
      user = User(first_name, last_name, age, weight, height, gender)
      tracker.set_user(user)
      st.success("✅ Profile saved successfully!")
      st.rerun()
  
  # Display current profile info if it exists
  if tracker.user:
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
      st.metric("BMI", tracker.user.calculate_bmi())
    with col2:
      st.metric("BMI Category", tracker.user.get_bmi_category())
    with col3:
      weight_change = tracker.user.get_weight_change()
      st.metric("Weight Change", f"{weight_change} kg")
    with col4:
      st.metric("Age", f"{tracker.user.age} years")

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
      st.metric(TOTAL_WORKOUTS, len(tracker.workouts))
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