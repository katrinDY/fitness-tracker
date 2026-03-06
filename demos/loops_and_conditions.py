from datetime import datetime, timedelta
from workout_tracker import WorkoutTracker

def categorize_workouts_by_intensity(tracker):
  print("\n🔁 LOOP EXAMPLE 1: Iterate through workouts and categorize")

  low_intensity = []
  medium_intensity = []
  high_intensity = []

  for workout in tracker.workouts:
    intensity = workout.get_intensity()
    if intensity == "Low":
      low_intensity.append(workout)
    elif intensity == "Medium":
      medium_intensity.append(workout)
    else:
      high_intensity.append(workout)

  print(f"Low intensity: {len(low_intensity)} workouts")
  print(f"Medium intensity: {len(medium_intensity)} workouts")
  print(f"High intensity: {len(high_intensity)} workouts")

def calculate_weekly_totals(tracker):
  print("\n🔁 LOOP EXAMPLE 2: Calculate weekly totals")

  today = datetime.now()
  week_start = today - timedelta(days=today.weekday())

  for i in range(7):
    day = week_start + timedelta(days=i)
    day_workouts = [w for w in tracker.workouts if w.date.date() == day.date()]
    if day_workouts:
      total_calories = sum(w.calories_burned for w in day_workouts)
      print(f"{day.strftime('%A')}: {len(day_workouts)} workouts, {total_calories} cal")
    else:
      print(f"{day.strftime('%A')}: Rest day")

def print_bmi_recommendations(tracker):
  print("\n⚖️ CONDITIONAL EXAMPLE: BMI-based recommendations")

  if tracker.user:
    bmi = tracker.user.calculate_bmi()
    category = tracker.user.get_bmi_category()
    print(f"BMI: {bmi} ({category})")
    if bmi < 18.5:
      print("💡 Recommendation: Focus on strength training and nutrition")
    elif 18.5 <= bmi < 25:
      print("💡 Recommendation: Maintain current routine")
    elif 25 <= bmi < 30:
      print("💡 Recommendation: Increase cardio and monitor diet")
    else:
      print("💡 Recommendation: Consult healthcare provider for guidance")

def print_top_calorie_workouts(tracker):
  print("\n🔁 LOOP EXAMPLE 3: Sort workouts by calories burned")

  sorted_workouts = sorted(tracker.workouts, 
                      key=lambda w: w.calories_burned, 
                      reverse=True)
  print("Top 3 calorie-burning workouts:")

  for i, workout in enumerate(sorted_workouts[:3], 1):
    print(f"{i}. {workout.workout_type.capitalize()}: "
      f"{workout.calories_burned} cal ({workout.duration} min)")

def print_goal_achievement(tracker):
  print("\n✅ CONDITIONAL EXAMPLE: Goal achievement check")

  for goal in tracker.goals:
    progress = goal.get_progress_percentage()
    if goal.completed:
      print(f"🎉 {goal.description}: COMPLETED!")
    elif progress >= 75:
      print(f"💪 {goal.description}: Almost there! ({progress}%)")
    elif progress >= 50:
      print(f"⚡ {goal.description}: Good progress ({progress}%)")
    else:
      print(f"🎯 {goal.description}: Keep going! ({progress}%)")

def demo_loops_and_conditionals():
  """Demonstrate use of loops and conditional expressions."""
  print("DEMO: LOOPS & CONDITIONALS")
  tracker = WorkoutTracker("demo_fitness_data.json")
  categorize_workouts_by_intensity(tracker)
  calculate_weekly_totals(tracker)
  print_bmi_recommendations(tracker)
  print_top_calorie_workouts(tracker)
  print_goal_achievement(tracker)

if __name__ == "__main__":
  demo_loops_and_conditionals()