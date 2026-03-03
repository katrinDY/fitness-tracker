import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User

def demo_user_class():
  print("👤 DEMO: User Class")
  
  # Create a user
  user = User("Ivan", "Ivanov", 30, 80, 180, "male")
  
  # Print user name
  print(f"The created user is {user.first_name} {user.last_name}")

  # Calculate BMI
  bmi = user.calculate_bmi()
  print(f"User BMI is: {bmi}")

  # Get BMI category
  bmi_category = user.get_bmi_category()
  print(f"User BMI category is: {bmi_category}")

  # Print current user weight
  current_weight = user.weight
  print(f"The current user weight is: {current_weight} kg")

  # Update user weight and check weight change
  new_user_weight = 90
  user.update_weight(new_user_weight)
  user.get_weight_change()
  print(f"User weight updated to: {user.weight} kg")
  

demo_user_class()