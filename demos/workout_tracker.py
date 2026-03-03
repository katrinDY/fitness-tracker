import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User
from models.workout_tracker import WorkoutTracker
from models.workout import Workout
from models.goal import Goal

def demo_workout_tracker():
  print("DEMO: WORKOUT TRACKER CLASS")
  
  # Create tracker with demo data file
  tracker = WorkoutTracker(f"demo_fitness_data_{datetime.now().timestamp()}.json")
  
  # Set user
  user = User("Maria", "Georgieva", 25, 65, 168, "female")
  tracker.set_user(user)
  print(f"User set: {user.first_name} {user.last_name}")
  
  # Add workouts
  workout_data = [
    ("running", 30),
    ("yoga", 45),
    ("gym", 60),
    ("cycling", 40),
    ("swimming", 35),
  ]
  
  print(f"\n📝 Adding {len(workout_data)} workouts...")
  for i, (wtype, duration) in enumerate(workout_data):
    # Spread workouts across different days
    date = datetime.now() - timedelta(days=len(workout_data) - i - 1)
    workout = Workout(wtype, duration, date=date, user_weight=user.weight)
    tracker.add_workout(workout)
  
  print(f"✅ Added {len(tracker.workouts)} workouts")
  
  # Add a goal
  goal = Goal(
    goal_type="workout_count",
    target_value=10,
    current_value=len(tracker.workouts),
    description="Reach 10 workouts"
  )
  tracker.add_goal(goal)
  print(f"\n🎯 Goal added: {goal.description}")
  print(f"   Progress: {goal.get_progress_percentage()}%")
  
  # Get statistics
  print("\n📊 STATISTICS")
  
  stats = tracker.get_total_stats()
  print(f"Total workouts: {stats['total_workouts']}")
  print(f"Total duration: {stats['total_duration']} minutes")
  print(f"Total calories: {stats['total_calories']} cal")
  print(f"Average duration: {stats['avg_duration']} min/workout")
  print(f"Most common workout: {stats['most_common_workout']}")
  print(f"Current streak: {stats['current_streak']} days 🔥")
  
  # Weekly summary
  print("\n📅 WEEKLY SUMMARY")
  
  weekly = tracker.get_weekly_summary()
  print(f"Workouts this week: {weekly['workout_count']}")
  print(f"Total duration: {weekly['total_duration']} minutes")
  print(f"Total calories: {weekly['total_calories']} cal")
  
  # Filter workouts
  print("\n🔍 FILTERING EXAMPLES")
  
  running_workouts = tracker.get_workouts_by_type("running")
  print(f"Running workouts: {len(running_workouts)}")
  
  # Export to CSV
  print("\n💾 DATA EXPORT")
  
  if tracker.export_to_csv("demo_export.csv"):
    print("✅ Data exported to demo_export.csv")

if __name__ == "__main__":
  demo_workout_tracker()