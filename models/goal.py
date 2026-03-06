from datetime import datetime
from typing import Optional, Dict

class Goal:
  """
    Represents a fitness goal with progress tracking.
  """
  
  def __init__(self, goal_type: str, target_value: float, current_value: float = 0, deadline: datetime = None, description: str = ''):
    """
      Initialize a Goal instance.
      
      Args:
        goal_type: Type of goal (weight_loss, workout_count, total_calories, etc.)
        target_value: Target value to achieve
        current_value: Current progress value
        deadline: Optional deadline for the goal
        description: Description of the goal
    """
    self.goal_type = goal_type
    self.target_value = target_value
    self.current_value = current_value
    self.deadline = deadline
    self.description = description
    self.created_at = datetime.now()
    self.completed = False
    self.completed_at = None
  
  def update_progress(self, value: float) -> None:
    """
      Update current progress value.
      
      Args:
        value: New current value
    """
    self.current_value = value
    if self.current_value >= self.target_value:
      self.mark_completed()
  
  def get_progress_percentage(self) -> float:
    """
      Calculate progress percentage.
      
      Returns:
        Progress as percentage (0-100)
    """
    if self.target_value == 0:
      return 0.0
    percentage = (self.current_value / self.target_value) * 100
    return min(round(percentage, 1), 100)

  def mark_completed(self) -> None:
    """Mark the goal as completed."""
    self.completed = True
    self.completed_at = datetime.now()
  
  def is_overdue(self) -> bool:
    """
      Check if goal is overdue.
      
      Returns:
        True if deadline has passed and goal not completed
    """
    if not self.deadline or self.completed:
      return False
    return datetime.now() > self.deadline
  
  def days_remaining(self) -> Optional[int]:
    """
      Calculate days remaining until deadline.
      
      Returns:
        Number of days remaining, or None if no deadline
    """
    if not self.deadline:
      return None
    delta = self.deadline - datetime.now()
    return max(0, delta.days)
  
  def to_dict(self) -> Dict:
    """Convert goal data to dictionary for serialization."""
    return {
      'goal_type': self.goal_type,
      'target_value': self.target_value,
      'current_value': self.current_value,
      'deadline': self.deadline.isoformat() if self.deadline else None,
      'description': self.description,
      'created_at': self.created_at.isoformat(),
      'completed': self.completed,
      'completed_at': self.completed_at.isoformat() if self.completed_at else None
    }
  
  @classmethod
  def from_dict(cls, data: Dict) -> 'Goal':
    """Create a Goal instance from a dictionary."""
    goal = cls(
      goal_type=data['goal_type'],
      target_value=data['target_value'],
      current_value=data['current_value'],
      deadline=datetime.fromisoformat(data['deadline']) if data['deadline'] else None,
      description=data['description'],
    )
    goal.created_at = datetime.fromisoformat(data['created_at'])
    goal.completed = data['completed']
    goal.completed_at = datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
    return goal