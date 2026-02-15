from datetime import datetime
from typing import Dict

class User():
  """
    Represents a user profile with personal information and fitness metrics.
  """
  def __init__(self, first_name: str, last_name: str, age: int, weight: float, height: float, gender: str):
    """
      Initialize a User instance.
      
      Args:
        name: User's full name
        age: User's age in years
        weight: Current weight in kg
        height: Height in cm
        gender: 'male' or 'female'
    """
    self.first_name = first_name
    self.last_name = last_name
    self.age = age
    self.weight = weight
    self.height = height
    self.gender = gender
    self.created_at = datetime.now()
    self.weight_history = [(datetime.now(), weight)]
  
  def calculate_bmi(self) -> float:
    """
      Calculate Body Mass Index (BMI).
      
      Returns:
        BMI value rounded to 2 decimal places
    """
    height_m = self.height / 100  # Convert height from cm to meters
    bmi = self.weight / (height_m ** 2)
    return round(bmi, 2)

  def get_bmi_category(self) -> str:
    """
      Get BMI category based on WHO standards.
      
      Returns:
        BMI category as string
    """
    bmi = self.calculate_bmi()
    if bmi < 18.5:
      return "Underweight"
    elif 18.5 <= bmi < 25:
      return "Normal weight"
    elif 25 <= bmi < 30:
      return "Overweight"
    else:
      return "Obese"
  
  def update_weight(self, new_weight: float) -> None:
    """
      Update user's weight and add to weight history.
      
      Args:
        new_weight: New weight in kg
    """
    self.weight = new_weight
    self.weight_history.append((datetime.now(), new_weight))
  
  def get_weight_change(self) -> float:
    """
      Calculate weight change since first record.
      
      Returns:
        Weight change in kg (negative = weight loss, positive = weight gain)
    """
    if len(self.weight_history) < 2:
      return 0.0
    first_weight = self.weight_history[0][1]
    current_weight = self.weight_history[-1][1]
    return round(current_weight - first_weight, 2)
  
  def data_to_dict(self) -> dict:
    """Convert user data to dictionary for serialization."""
    return {
      'first_name': self.first_name,
      'last_name': self.last_name,
      'age': self.age,
      'weight': self.weight,
      'height': self.height,
      'gender': self.gender,
      'created_at': self.created_at.isoformat(),
      'weight_history': [(timestamp.isoformat(), weight) for timestamp, weight in self.weight_history]
    }
  
  @classmethod
  def from_dict(cls, data: Dict) -> 'User':
    """Create User instance from dictionary."""
    user = cls(
      name=data['name'],
      age=data['age'],
      weight=data['weight'],
      height=data['height'],
      gender=data['gender']
    )

    user.created_at = datetime.fromisoformat(data['created_at'])
    user.weight_history = [(datetime.fromisoformat(dt), w) for dt, w in data['weight_history']]
    return user