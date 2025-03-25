from django.db import models
from users.models import User


class Task(models.Model):

    """
    Represents a task in the system that can be assigned to multiple users.
    
    Attributes:
        name (str): The name/title of the task
        description (str): Detailed description of the task
        created_at (datetime): Auto-set timestamp when task is created
        task_type (str): Category of task (Personal, College, Work, Other)
        completed_at (datetime): Timestamp when task was completed
        status (str): Current status of the task (Pending, In Progress, Completed)
        assigned_users (QuerySet[User]): Users assigned to this task
    """

    class TaskType(models.TextChoices):
        """Enumeration of valid task types"""
        PERSONAL = 'P', 'Personal'
        COLLEGE = 'C', 'College'
        WORK = 'W', 'Work'
        OTHER = 'O', 'Other'

    class Status(models.TextChoices):
        """Enumeration of valid task statuses"""
        PENDING = 'P', 'Pending'
        IN_PROGRESS = 'I', 'In Progress'
        COMPLETED = 'C', 'Completed'

    
    name = models.CharField(max_length=100) # Name of task
    description = models.TextField(blank=True, null=True) # Description of task
    created_at = models.DateTimeField(auto_now_add=True) # Auto-set timestamp when task is created
    task_type = models.CharField(max_length=1, choices=TaskType.choices, default=TaskType.OTHER) # Category of the task (default: OTHER)
    completed_at = models.DateTimeField(blank=True, null=True) # Timestamp when task was marked completed
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING) # Current progress status of the task (default: PENDING)
    assigned_users = models.ManyToManyField(User, related_name='tasks') # Users assigned to this task
    
    def __str__(self) -> str:
        """String representation of the task"""
        return self.name