"""
Fitness Tracker - Command Line Interface
Main entry point for the CLI version of the fitness tracker application.
"""

from models import User, Workout, Goal, WorkoutTracker
from datetime import datetime, timedelta
import sys

INVALID_NUMBER_MESSAGE = "❌ Please enter a valid number."
YOUR_CHOICE_PROMPT = "\nYour choice: "
NO_WORKOUTS_MESSAGE = "\n❌ No workouts recorded yet."
INVALID_CHOICE_MESSAGE = "❌ Invalid choice."

def print_header(text: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def print_menu() -> None:
    """Display the main menu."""
    print("\n📊 FITNESS TRACKER - MAIN MENU")
    print("-" * 50)
    print("1. 👤 View/Edit Profile")
    print("2. 💪 Add Workout")
    print("3. 📋 View Workout History")
    print("4. 📈 View Statistics")
    print("5. 🎯 Manage Goals")
    print("6. 📊 Weekly Summary")
    print("7. 💾 Export Data")
    print("8. 🚪 Exit")
    print("-" * 50)

def setup_user(tracker: WorkoutTracker) -> None:
  """Create or update user profile."""
  print_header("USER PROFILE SETUP")
  
  first_name = input("Enter your first name: ").strip()
  last_name = input("Enter your last name: ").strip()
  
  while True:
    try:
      age = int(input("Enter your age: "))
      if age < 10 or age > 120:
        print("❌ Age must be between 10 and 120.")
        continue
      break
    except ValueError:
      print()
    
  while True:
    try:
      weight = float(input("Enter your weight (kg): "))
      if weight < 20 or weight > 300:
        print("❌ Weight must be between 20 and 300 kg.")
        continue
      break
    except ValueError:
      print(INVALID_NUMBER_MESSAGE)
  
  while True:
    try:
      height = float(input("Enter your height (cm): "))
      if height < 100 or height > 250:
        print("❌ Height must be between 100 and 250 cm.")
        continue
      break
    except ValueError:
      print(INVALID_NUMBER_MESSAGE)
  
  while True:
    gender = input("Enter your gender (male/female): ").strip().lower()
    if gender in ['male', 'female']:
      break
    print("❌ Please enter 'male' or 'female'.")
  
  user = User(first_name, last_name, age, weight, height, gender)
  tracker.set_user(user)
  tracker.save_data()
  
  print("\n✅ Profile created successfully!")
  print(f"📊 Your BMI: {user.calculate_bmi()} ({user.get_bmi_category()})")


def view_profile(tracker: WorkoutTracker) -> None:
  """Display user profile information."""
  if not tracker.user:
    print("\n❌ No user profile found. Please create one first.")
    return
  
  user = tracker.user
  print_header("YOUR PROFILE")
  print(f"Name: {user.first_name} {user.last_name}")
  print(f"Age: {user.age} years")
  print(f"Weight: {user.weight} kg")
  print(f"Height: {user.height} cm")
  print(f"Gender: {user.gender.capitalize()}")
  print(f"\n📊 BMI: {user.calculate_bmi()} ({user.get_bmi_category()})")
  
  weight_change = user.get_weight_change()
  if weight_change != 0:
    sign = "+" if weight_change > 0 else ""
    print(f"📉 Weight change: {sign}{weight_change} kg")
  
  print("\nOptions:")
  print("1. Update weight")
  print("2. Back to main menu")
  
  choice = input(YOUR_CHOICE_PROMPT).strip()
  if choice == "1":
    try:
      new_weight = float(input("Enter new weight (kg): "))
      user.update_weight(new_weight)
      tracker.save_data()
      print(f"✅ Weight updated! New BMI: {user.calculate_bmi()}")
    except ValueError:
      print("❌ Invalid weight entered.")


def add_workout(tracker: WorkoutTracker) -> None:
  """Add a new workout session."""
  if not tracker.user:
    print("\n❌ Please create a user profile first.")
    return
  
  print_header("ADD NEW WORKOUT")
  
  # Display available workout types
  workout_types = list(Workout.CALORIE_RATES.keys())
  print("Available workout types:")
  for i, wtype in enumerate(workout_types, 1):
    print(f"{i}. {wtype.capitalize()}")
  
  # Select workout type
  while True:
    try:
      choice = int(input("\nSelect workout type (number): "))
      if 1 <= choice <= len(workout_types):
        workout_type = workout_types[choice - 1]
        break
      print(f"❌ Please enter a number between 1 and {len(workout_types)}.")
    except ValueError:
      print(INVALID_NUMBER_MESSAGE)
    
  # Enter duration
  while True:
    try:
      duration = int(input("Enter duration (minutes): "))
      if duration < 1:
        print("❌ Duration must be at least 1 minute.")
        continue
      if duration > 480:  # 8 hours max
        print("❌ Duration seems too long. Max 480 minutes.")
        continue
      break
    except ValueError:
      print(INVALID_NUMBER_MESSAGE)
  
  # Optional notes
  notes = input("Add notes (optional, press Enter to skip): ").strip()
  
  # Create workout
  workout = Workout(
    workout_type=workout_type,
    duration=duration,
    notes=notes,
    user_weight=tracker.user.weight
  )
  
  tracker.add_workout(workout)
  
  print("\n✅ Workout added successfully!")
  print(f"🔥 Calories burned: {workout.calories_burned}")
  print(f"💪 Intensity: {workout.get_intensity()}")
  
  # Check if any goals were completed
  for goal in tracker.goals:
    if goal.completed and goal.completed_at and \
    (datetime.now() - goal.completed_at).total_seconds() < 5:
      print(f"\n🎉 Congratulations! Goal completed: {goal.description}")


def view_workout_history(tracker: WorkoutTracker) -> None:
  """Display workout history with filtering options."""
  if not tracker.workouts:
    print(NO_WORKOUTS_MESSAGE)
    return
  
  print_header("WORKOUT HISTORY")
  print("1. View all workouts")
  print("2. Filter by workout type")
  print("3. View this week")
  print("4. View this month")
  
  choice = input(YOUR_CHOICE_PROMPT).strip()
  
  workouts_to_show = []
  
  if choice == "1":
    workouts_to_show = tracker.workouts
  elif choice == "2":
    workout_types = list({w.workout_type for w in tracker.workouts})
    print("\nAvailable types:")
    for i, wtype in enumerate(workout_types, 1):
      print(f"{i}. {wtype.capitalize()}")
    
    try:
      type_choice = int(input("\nSelect type: "))
      if 1 <= type_choice <= len(workout_types):
        selected_type = workout_types[type_choice - 1]
        workouts_to_show = tracker.get_workouts_by_type(selected_type)
    except ValueError:
      print(INVALID_CHOICE_MESSAGE)
      return
  elif choice == "3":
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    workouts_to_show = tracker.get_workouts_by_date_range(week_start, today)
  elif choice == "4":
    today = datetime.now()
    month_start = today.replace(day=1)
    workouts_to_show = tracker.get_workouts_by_date_range(month_start, today)
  else:
    print(INVALID_CHOICE_MESSAGE)
    return
  
  if not workouts_to_show:
    print("\n❌ No workouts found for this selection.")
    return
  
  # Sort by date (newest first)
  workouts_to_show.sort(key=lambda w: w.date, reverse=True)
  
  print(f"\n📋 Found {len(workouts_to_show)} workout(s):")
  print("-" * 80)
  print(f"{'Date':<20} {'Type':<15} {'Duration':<12} {'Calories':<12} {'Notes':<20}")
  print("-" * 80)
  
  for workout in workouts_to_show:
      date_str = workout.date.strftime("%Y-%m-%d %H:%M")
      notes_short = workout.notes[:17] + "..." if len(workout.notes) > 20 else workout.notes
      print(f"{date_str:<20} {workout.workout_type.capitalize():<15} "
          f"{workout.duration} min{'':<7} {workout.calories_burned} cal{'':<7} {notes_short:<20}")
  
  print("-" * 80)
  total_duration = sum(w.duration for w in workouts_to_show)
  total_calories = sum(w.calories_burned for w in workouts_to_show)
  print(f"TOTAL: {len(workouts_to_show)} workouts | {total_duration} minutes | {total_calories} calories")


def view_statistics(tracker: WorkoutTracker) -> None:
  """Display comprehensive statistics."""
  if not tracker.workouts:
    print(NO_WORKOUTS_MESSAGE)
    return
  
  print_header("YOUR STATISTICS")
  
  stats = tracker.get_total_stats()
  
  print("\n🏆 ALL-TIME STATS:")
  print(f"   Total Workouts: {stats['total_workouts']}")
  print(f"   Total Duration: {stats['total_duration']} minutes ({stats['total_duration'] // 60} hours)")
  print(f"   Total Calories: {stats['total_calories']:,} cal")
  print(f"   Average Duration: {stats['avg_duration']} min/workout")
  print(f"   Most Common: {stats['most_common_workout'].capitalize() if stats['most_common_workout'] else 'N/A'}")
  print(f"   Current Streak: {stats['current_streak']} days 🔥")
  
  # Weekly stats
  weekly = tracker.get_weekly_summary()
  print("\n📅 THIS WEEK:")
  print(f"   Workouts: {weekly['workout_count']}")
  print(f"   Duration: {weekly['total_duration']} minutes")
  print(f"   Calories: {weekly['total_calories']} cal")
  if weekly['workout_types']:
    print("   Breakdown:", end=" ")
    for wtype, count in weekly['workout_types'].items():
      print(f"{wtype.capitalize()}: {count}", end=" | ")
    print()
  
  # Monthly stats
  monthly = tracker.get_monthly_summary()
  print("\n📆 THIS MONTH:")
  print(f"   Workouts: {monthly['workout_count']}")
  print(f"   Duration: {monthly['total_duration']} minutes")
  print(f"   Calories: {monthly['total_calories']:,} cal")


def manage_goals(tracker: WorkoutTracker) -> None:
  """Manage fitness goals."""
  print_header("GOAL MANAGEMENT")
  print("1. View active goals")
  print("2. View completed goals")
  print("3. Add new goal")
  print("4. Back to main menu")
  
  choice = input(YOUR_CHOICE_PROMPT).strip()
  
  if choice == "1":
    active_goals = tracker.get_active_goals()
    if not active_goals:
      print("\n❌ No active goals. Create one to get started!")
      return
    
    print("\n🎯 ACTIVE GOALS:")
    for i, goal in enumerate(active_goals, 1):
      print(f"\n{i}. {goal.description}")
      print(f"   Progress: {goal.get_progress_percentage()}% "
        f"({goal.current_value}/{goal.target_value})")
      if goal.deadline:
        days = goal.days_remaining()
        if goal.is_overdue():
          print("   ⚠️  OVERDUE!")
        else:
          print(f"   ⏰ {days} days remaining")
  
  elif choice == "2":
    completed_goals = tracker.get_completed_goals()
    if not completed_goals:
      print("\n❌ No completed goals yet. Keep working!")
      return
    
    print("\n✅ COMPLETED GOALS:")
    for i, goal in enumerate(completed_goals, 1):
      completed_date = goal.completed_at.strftime("%Y-%m-%d")
      print(f"{i}. {goal.description} - Completed on {completed_date}")
  
  elif choice == "3":
    add_new_goal(tracker)


def add_new_goal(tracker: WorkoutTracker) -> None:
  """Create a new fitness goal."""
  print("\n📝 CREATE NEW GOAL")
  
  print("\nGoal Types:")
  print("1. Workout Count (e.g., 20 workouts)")
  print("2. Total Calories (e.g., burn 10,000 calories)")
  print("3. Total Duration (e.g., 1000 minutes)")
  
  goal_types = {
      "1": "workout_count",
      "2": "total_calories",
      "3": "total_duration"
  }
    
  choice = input("\nSelect goal type: ").strip()
  if choice not in goal_types:
    print(INVALID_CHOICE_MESSAGE)
    return
  
  goal_type = goal_types[choice]
  
  # Get target value
  while True:
    try:
      target = float(input("Enter target value: "))
      if target <= 0:
        print("❌ Target must be positive.")
        continue
      break
    except ValueError:
      print(INVALID_NUMBER_MESSAGE)
  
  # Get current value from existing data
  current_value = 0
  if goal_type == "workout_count":
    current_value = len(tracker.workouts)
  elif goal_type == "total_calories":
    current_value = sum(w.calories_burned for w in tracker.workouts)
  elif goal_type == "total_duration":
    current_value = sum(w.duration for w in tracker.workouts)
    
  # Optional deadline
  has_deadline = input("Set a deadline? (y/n): ").strip().lower()
  deadline = None
  if has_deadline == 'y':
    while True:
      try:
        days = int(input("How many days from now? "))
        if days < 1:
          print("❌ Must be at least 1 day.")
          continue
        deadline = datetime.now() + timedelta(days=days)
        break
      except ValueError:
        print(INVALID_NUMBER_MESSAGE)
  
  description = input("Goal description: ").strip()
  
  goal = Goal(
    goal_type=goal_type,
    target_value=target,
    deadline=deadline,
    description=description
  )
  goal.update_progress(current_value)

  tracker.add_goal(goal)
  print(f"\n✅ Goal created! Current progress: {goal.get_progress_percentage()}%")


def weekly_summary(tracker: WorkoutTracker) -> None:
  """Display detailed weekly summary."""
  if not tracker.workouts:
    print(NO_WORKOUTS_MESSAGE)
    return
  
  summary = tracker.get_weekly_summary()
  
  print_header("WEEKLY SUMMARY")
  print(f"Week starting: {summary['week_start'].strftime('%Y-%m-%d')}")
  print("\n📊 Overview:")
  print(f"   Total Workouts: {summary['workout_count']}")
  print(f"   Total Duration: {summary['total_duration']} minutes")
  print(f"   Total Calories: {summary['total_calories']:,} cal")
  print(f"   Average Duration: {summary['avg_duration']} min/workout")
  
  if summary['workout_types']:
    print("\n💪 Workout Breakdown:")
    for wtype, count in summary['workout_types'].items():
      percentage = (count / summary['workout_count'] * 100)
      print(f"   {wtype.capitalize()}: {count} ({percentage:.1f}%)")
  
  # Daily breakdown
  today = datetime.now()
  week_start = today - timedelta(days=today.weekday())
  
  print("\n📅 Daily Activity:")
  for i in range(7):
    day = week_start + timedelta(days=i)
    day_workouts = [w for w in tracker.workouts 
              if w.date.date() == day.date()]
    
    day_name = day.strftime("%a %d/%m")
    if day_workouts:
      total_min = sum(w.duration for w in day_workouts)
      print(f"   {day_name}: ✅ {len(day_workouts)} workout(s) - {total_min} min")
    else:
        print(f"   {day_name}: ⚪ Rest day")


def export_data(tracker: WorkoutTracker) -> None:
  """Export data to CSV."""
  if not tracker.workouts:
    print("\n❌ No workouts to export.")
    return
  
  print_header("EXPORT DATA")
  
  filename = input("Enter filename (or press Enter for 'workouts_export.csv'): ").strip()
  if not filename:
    filename = "workouts_export.csv"
  
  if not filename.endswith('.csv'):
    filename += '.csv'
  
  if tracker.export_to_csv(filename):
    print(f"\n✅ Data exported successfully to {filename}!")
  else:
    print("\n❌ Export failed.")


def main():
  """Main application loop."""
  tracker = WorkoutTracker()
  
  print("\n" + "=" * 50)
  print("  💪 WELCOME TO FITNESS TRACKER")
  print("=" * 50)
  
  # Check if user exists
  if not tracker.user:
    print("\n👋 First time here? Let's set up your profile!")
    setup_user(tracker)
  else:
    print(f"\n👋 Welcome back, {tracker.user.first_name} {tracker.user.last_name}!")
    
    # Show quick stats
    if tracker.workouts:
      streak = tracker.get_streak()
      if streak > 0:
        print(f"🔥 Current streak: {streak} days!")
  
  # Main loop
  while True:
      print_menu()
      choice = input(YOUR_CHOICE_PROMPT).strip()
      
      if choice == "1":
        if tracker.user:
          view_profile(tracker)
        else:
          setup_user(tracker)
      
      elif choice == "2":
        add_workout(tracker)
      
      elif choice == "3":
        view_workout_history(tracker)
      
      elif choice == "4":
        view_statistics(tracker)
      
      elif choice == "5":
        manage_goals(tracker)
      
      elif choice == "6":
        weekly_summary(tracker)
      
      elif choice == "7":
        export_data(tracker)
      
      elif choice == "8":
        print("\n👋 Thanks for using Fitness Tracker! Stay healthy! 💪")
        sys.exit(0)
      
      else:
        print("\n❌ Invalid choice. Please select 1-8.")
        
      input("\nPress Enter to continue...")


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print("\n\n👋 Goodbye!")
    sys.exit(0)
