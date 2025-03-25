from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.models import Task
from users.models import User
from datetime import datetime
from django.contrib.auth.hashers import check_password


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test users once for all tests
        cls.user1 = User.objects.create(username="user1", email="user1@test.com")
        cls.user2 = User.objects.create(username="user2", email="user2@test.com")

    def test_create_valid_task(self):
        """Test creating a task with valid data"""
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
    
    def test_missing_required_fields(self):
        """Test task without required fields"""
        with self.assertRaises(ValidationError):
            task = Task()  # No name or task_type
            task.full_clean()

    def test_invalid_task_type(self):
        """Test invalid task type choice"""
        with self.assertRaises(ValidationError):
            task = Task(
                name="Invalid Type",
                task_type="X"  
            )
            task.full_clean()
    
    def test_multiple_assignments(self):
        """Test assigning to multiple users"""
        task = Task.objects.create(
            name="Team Task",
            task_type="W"
        )
        task.assigned_users.add(self.user1, self.user2)
        
        self.assertEqual(task.assigned_users.count(), 2)
        self.assertIn(self.user1, task.assigned_users.all())