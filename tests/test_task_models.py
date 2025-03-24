from django.test import TestCase
from django.core.exceptions import ValidationError
from tasks.models import Task
from users.models import User
from datetime import datetime
from django.contrib.auth.hashers import check_password


class UserModelTest(TestCase):
    def setUp(self):
        # Common valid data
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_valid_user(self):
        """Test creating a user with all required fields"""
        user = User.objects.create_user(**self.valid_data)
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(check_password("testpass123", user.password))
        self.assertEqual(user.name, "Test User")  # Test @property
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_mobile_number_validation(self):
        """Test mobile number formatting"""
        # Valid case
        valid_user = User(
            **self.valid_data,
            mobile="1234567890"  # Valid format
        )
        valid_user.full_clean()  # Should not raise

        # Invalid case
        with self.assertRaises(ValidationError):
            invalid_user = User(
                **self.valid_data,
                mobile="111234567890" 
            )
            invalid_user.full_clean()

    def test_required_fields(self):
        """Test missing required fields"""
        required_fields = ['username', 'password']
        
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_data.copy()
                invalid_data.pop(field)
                
                with self.assertRaises(ValidationError):
                    user = User(**invalid_data)
                    user.full_clean()

    def test_password_hashed(self):
        """Test password is properly hashed"""
        raw_password = "testpass123"
        user = User.objects.create_user(**self.valid_data)
        self.assertTrue(check_password(raw_password, user.password))
        self.assertNotEqual(raw_password, user.password)  # Ensure hashing

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