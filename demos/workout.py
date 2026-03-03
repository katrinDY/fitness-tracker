import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.workout import Workout

def demo_workout_class():
  print("🏋️ DEMO: Workout Class")
  
  # Single workout
  print("\n🔹 Single Workout Example")
  # Create a workout
  workout = Workout("running", 30, notes="Morning jog in the park", user_weight=80)
  
  # Print workout type
  print(f"Workout type: {workout.workout_type}")
  
  # Print burned calories
  print(f"Calories burned: {workout.calories_burned:.2f} kcal")
  
  # Print workout intensity
  print(f"Workout intensity: {workout.get_intensity()}")
  
  # Multiple workout
  print("\n🔹 Multiple Workouts Examples")
  # Add multiple workouts and print details
  workouts = [
    Workout("gym", 45, notes="Full body workout"),
    Workout("yoga", 15, notes="Body stretch"),
  ]

  for w in workouts:
    print(f"\nWorkout type: {w.workout_type}")
    print(f"Calories burned: {w.calories_burned:.2f} kcal")
    print(f"Workout intensity: {w.get_intensity()}")
    print(f"Notes: {w.notes}")

demo_workout_class()