from datetime import datetime, timedelta
from typing import Optional, List, Dict
from user import User
from workout import Workout
from goal import Goal
import json

class WorkoutTracker:
  """
    Main tracker class that manages users, workouts, and goals.
    Handles data persistence and analytics.
  """
  
  def __init__(self, data_file: str = "fitness_data.json"):
    """
    Initialize WorkoutTracker.
    
    Args:
        data_file: Path to JSON file for data persistence
    """
    self.data_file = data_file
    self.user: Optional[User] = None
    self.workouts: List[Workout] = []
    self.goals: List[Goal] = []
    self.load_data()
  
  def set_user(self, user: User) -> None:
    """Set the user profile."""
    self.user = user
  
  def add_workout(self, workout: Workout) -> None:
    """
      Add a new workout to the tracker.
      
      Args:
        workout: Workout instance to add
    """
    self.workouts.append(workout)
    self._update_goals_from_workout(workout)
    self.save_data()
  
  def _update_goals_from_workout(self, workout: Workout) -> None:
    """Update relevant goals based on new workout."""
    for goal in self.goals:
      if goal.goal_type == "workout_count":
        goal.update_progress(goal.current_value + 1)
      elif goal.goal_type == "total_calories":
        goal.update_progress(goal.current_value + workout.calories_burned)
      elif goal.goal_type == "total_duration":
        goal.update_progress(goal.current_value + workout.duration)
  
  def get_workouts_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Workout]:
    """
    Get workouts within a date range.
    
    Args:
      start_date: Start of date range
      end_date: End of date range
        
    Returns:
      List of workouts in the date range
    """
    return [w for w in self.workouts if start_date <= w.date <= end_date]
  
  def get_workouts_by_type(self, workout_type: str) -> List[Workout]:
    """
    Get all workouts of a specific type.
    
    Args:
      workout_type: Type of workout to filter
        
    Returns:
      List of workouts matching the type
    """
    return [w for w in self.workouts if w.workout_type == workout_type.lower()]
  
  def get_weekly_summary(self) -> Dict:
    """
    Get summary statistics for the current week.
    
    Returns:
        Dictionary with weekly statistics
    """
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    weekly_workouts = self.get_workouts_by_date_range(week_start, today)
    
    total_duration = sum(w.duration for w in weekly_workouts)
    total_calories = sum(w.calories_burned for w in weekly_workouts)
    workout_count = len(weekly_workouts)
    
    workout_types = {}
    for w in weekly_workouts:
      workout_types[w.workout_type] = workout_types.get(w.workout_type, 0) + 1
    
    return {
      'week_start': week_start,
      'workout_count': workout_count,
      'total_duration': total_duration,
      'total_calories': total_calories,
      'avg_duration': round(total_duration / workout_count, 1) if workout_count > 0 else 0,
      'workout_types': workout_types
    }
    
  def get_monthly_summary(self) -> Dict:
    """
    Get summary statistics for the current month.
    
    Returns:
      Dictionary with monthly statistics
    """
    today = datetime.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    monthly_workouts = self.get_workouts_by_date_range(month_start, today)
    
    total_duration = sum(w.duration for w in monthly_workouts)
    total_calories = sum(w.calories_burned for w in monthly_workouts)
    workout_count = len(monthly_workouts)
    
    return {
      'month_start': month_start,
      'workout_count': workout_count,
      'total_duration': total_duration,
      'total_calories': total_calories,
      'avg_per_workout': round(total_calories / workout_count, 1) if workout_count > 0 else 0
    }
    
  def get_streak(self) -> int:
    """
    Calculate current workout streak (consecutive days with workouts).
    
    Returns:
      Number of consecutive days with at least one workout
    """
    if not self.workouts:
      return 0
    
    # Sort workouts by date
    sorted_workouts = sorted(self.workouts, key=lambda w: w.date, reverse=True)
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    streak = 0
    current_date = today
    
    # Get unique workout dates
    workout_dates = {w.date.replace(hour=0, minute=0, second=0, microsecond=0) for w in sorted_workouts}
    
    # Count consecutive days
    while current_date in workout_dates:
      streak += 1
      current_date -= timedelta(days=1)
    
    return streak
    
  def add_goal(self, goal: Goal) -> None:
    """Add a new goal to the tracker."""
    self.goals.append(goal)
    self.save_data()
  
  def get_active_goals(self) -> List[Goal]:
    """Get all active (not completed) goals."""
    return [g for g in self.goals if not g.completed]
  
  def get_completed_goals(self) -> List[Goal]:
    """Get all completed goals."""
    return [g for g in self.goals if g.completed]
    
  def save_data(self) -> None:
    """Save all data to JSON file."""
    data = {
      'user': self.user.to_dict() if self.user else None,
      'workouts': [w.to_dict() for w in self.workouts],
      'goals': [g.to_dict() for g in self.goals]
    }
    
    try:
      with open(self.data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving data: {e}")
    
  def load_data(self) -> None:
    """Load data from JSON file."""
    try:
      with open(self.data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

      if data.get('user'):
        self.user = User.from_dict(data['user'])
      
      self.workouts = [Workout.from_dict(w) for w in data.get('workouts', [])]
      self.goals = [Goal.from_dict(g) for g in data.get('goals', [])]
        
    except FileNotFoundError:
      # First run - no data file exists yet
      pass
    except Exception as e:
      print(f"Error loading data: {e}")
    
  def export_to_csv(self, filename: str = "workouts_export.csv") -> bool:
    """
    Export workouts to CSV file.
    
    Args:
      filename: Name of CSV file to create
    
    Returns:
      True if successful, False otherwise
    """
    try:
      import csv
      
      with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Type', 'Duration (min)', 'Calories', 'Notes'])

        for w in sorted(self.workouts, key=lambda x: x.date):
          writer.writerow([
            w.date.strftime('%Y-%m-%d %H:%M'),
            w.workout_type,
            w.duration,
            w.calories_burned,
            w.notes
          ])
      
      return True
    except Exception as e:
      print(f"Error exporting to CSV: {e}")
      return False
    
  def get_total_stats(self) -> Dict:
    """
    Get all-time statistics.
    
    Returns:
      Dictionary with overall statistics
    """
    if not self.workouts:
      return {
        'total_workouts': 0,
        'total_duration': 0,
        'total_calories': 0,
        'avg_duration': 0,
        'most_common_workout': None
      }
    
    total_duration = sum(w.duration for w in self.workouts)
    total_calories = sum(w.calories_burned for w in self.workouts)
    
    # Find most common workout type
    workout_counts = {}
    for w in self.workouts:
      workout_counts[w.workout_type] = workout_counts.get(w.workout_type, 0) + 1
    most_common = max(workout_counts.items(), key=lambda x: x[1])[0] if workout_counts else None
    
    return {
      'total_workouts': len(self.workouts),
      'total_duration': total_duration,
      'total_calories': total_calories,
      'avg_duration': round(total_duration / len(self.workouts), 1),
      'most_common_workout': most_common,
      'current_streak': self.get_streak()
    }
