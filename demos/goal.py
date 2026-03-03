from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.goal import Goal

def demo_goal_class():
  print("🎯 DEMO: Goal Class")

  # Create a goal
  goal = Goal(
    goal_type="workout_count",
    target_value=20,
    current_value=5,
    deadline=datetime.now() + timedelta(days=30),
    description="Complete 20 workouts this month"
  )

  # Print goal description
  print(f"Goal: {goal.description}")

  # Print progress percentage
  print(f"Progress: {goal.get_progress_percentage()}%")

  # Print days remaining
  print(f"Days remaining: {goal.days_remaining()}")

  # Update progress until goal is completed
  for _ in range(3):
    goal.update_progress(goal.current_value + 5)
    print(f"Updated progress: {goal.get_progress_percentage()}%")

  if goal.completed:
    print("🎉 Goal completed!")

if __name__ == "__main__":
  demo_goal_class()
