from datetime import datetime
from typing import Dict

class Workout():
  """
    Represents a single workout session with details and calorie calculation.
  """
  
  # Calorie burn rates per minute by activity (Metabolic Equivalent of Task values approximation)
  CALORIE_RATES = {
      'running': 10.0,
      'cycling': 8.0,
      'swimming': 9.0,
      'gym': 6.0,
      'yoga': 3.0,
      'walking': 4.0,
      'hiit': 12.0,
      'dancing': 5.0
  }

  def __init__(self, workout_type: str, duration: int, date: datetime = None, notes: str = '', user_weight: float = 70):
    """
      Initialize a Workout instance.
      
      Args:
        workout_type: Type of workout (running, cycling, gym, etc.)
        duration: Duration in minutes
        date: Date of workout (defaults to now)
        notes: Optional notes about the workout
        user_weight: User's weight in kg (for calorie calculation)
    """
    self.workout_type = workout_type
    self.duration = duration
    self.date = date if date else datetime.now()
    self.notes = notes
    self.user_weight = user_weight
    self.calories_burned = self.calculate_calories()
  
  def calculate_calories(self):
    """
      Calculate calories burned based on workout type, duration, and user weight.
      Formula: (Metabolic Equivalent of Task * weight in kg * duration in hours)
      
      Returns:
        Estimated calories burned
    """
    rate = self.CALORIE_RATES.get(self.workout_type, 5.0)  # Default to 5.0 if workout type is unknown
    calories = rate * self.duration * (self.user_weight / 60)  # Convert duration to hours and weight to kg
    return calories

  def get_intensity(self):
    """
      Determine workout intensity based on calorie burn rate.
      
      Returns:
        Intensity level: Low, Medium, or High
    """
    rate = self.CALORIE_RATES.get(self.workout_type, 5.0)
    if rate < 5:
      return "Low"
    elif rate < 9:
      return "Medium"
    else:
      return "High"
  
  def data_to_dict(self):
    """Convert workout data to dictionary for serialization."""
    return {
      'workout_type': self.workout_type,
      'duration': self.duration,
      'date': self.date.isoformat(),
      'notes': self.notes,
      'user_weight': self.user_weight,
      'calories_burned': self.calories_burned
    }
  
  @classmethod
  def from_dict(cls, data: Dict) -> 'Workout':
    workout = cls(
      workout_type=data['workout_type'],
      duration=data['duration'],
      date=datetime.fromisoformat(data['date']),
      notes=data['notes'],
      user_weight=data['user_weight']
    )
    return workout
  
  def __str__(self) -> str:
    """
      Returned string representation of the workout.
      Automatically called when printing the workout instance.
    """
    return f"{self.workout_type.capitalize()} - {self.duration} min - {self.calories_burned} cal"