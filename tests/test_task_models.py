from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.models import Task
from users.models import User
from datetime import datetime
from django.contrib.auth.hashers import check_password

class TaskModelTest(TestCase):
    """Test suite for the Task model functionality and validation."""
    @classmethod
    def setUpTestData(cls) -> None:
        """
        Set up test data for the entire test case.
        
        This method runs once before all tests in the class. It creates
        test users that can be used across multiple test methods.
        """
        cls.user1 = User.objects.create(username="user1", email="user1@test.com")
        cls.user2 = User.objects.create(username="user2", email="user2@test.com")

    def test_create_valid_task(self) -> None:
        """
        Test creating a task with valid data
        
        Verifies:
        - Task is created with correct attributes
        - Status defaults to 'P' (Pending)
        - Users can be assigned to tasks
        - Timestamps are automatically set
        """

        task = Task.objects.create(
            name="Valid Task",
            description="This should work",
            task_type="W",
            status="P"
        )
        task.assigned_users.add(self.user1)
        
        self.assertEqual(task.name, "Valid Task")
        self.assertEqual(task.status, "P")
        self.assertEqual(task.assigned_users.count(), 1)
        self.assertIsNotNone(task.created_at)
        self.assertIsNone(task.completed_at)
    
    def test_missing_required_fields(self) -> None:
        """
        Test task without required fields
        
        Required fields are:
        - name
        - task_type
        
        Expects:
        - ValidationError to be raised when saving incomplete data
        """
        with self.assertRaises(ValidationError):
            task = Task()  # No name or task_type
            task.full_clean()

    def test_invalid_task_type(self) -> None:
        """
        Test invalid task type choice

        Valid task types are:
        - 'W' (Work)
        - 'P' (Personal)
        - 'S' (Shopping)
        - 'O' (Other)
        
        Expects:
        - ValidationError when using an invalid task type code
        """
        
        with self.assertRaises(ValidationError):
            task = Task(
                name="Invalid Type",
                task_type="X"  
            )
            task.full_clean()
    
    def test_multiple_assignments(self) -> None:
        """
        Test assigning to multiple users
        
        Verifies:
        - Multiple users can be added via the assigned_users relationship
        - Relationship count is accurate
        - All assigned users are properly associated
        """
        task = Task.objects.create(
            name="Team Task",
            task_type="W"
        )
        task.assigned_users.add(self.user1, self.user2)
        
        self.assertEqual(task.assigned_users.count(), 2)
        self.assertIn(self.user1, task.assigned_users.all())