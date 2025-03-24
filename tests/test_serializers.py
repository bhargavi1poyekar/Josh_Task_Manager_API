from django.test import TestCase
from rest_framework.exceptions import ValidationError
from tasks.models import User, Task
from tasks.serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskAssignSerializer
)
from django.utils import timezone

class TaskSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='taskuser')
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status='P'
        )
        self.task.assigned_users.add(self.user)

    def test_serializer_output(self):
        serializer = TaskSerializer(self.task)
        expected_fields = [
            'id', 'name', 'description', 'created_at',
            'task_type', 'completed_at', 'status', 'assigned_users'
        ]
        self.assertEqual(list(serializer.data.keys()), expected_fields)
        self.assertEqual(len(serializer.data['assigned_users']), 1)

    def test_status_display(self):
        """Test status codes are properly displayed"""
        self.task.status = 'C'
        self.task.completed_at = timezone.now()
        serializer = TaskSerializer(self.task)
        self.assertEqual(serializer.data['status'], 'C')
        self.assertIsNotNone(serializer.data['completed_at'])

class TaskCreateSerializerTest(TestCase):
    def test_valid_creation(self):
        data = {
            'name': 'New Task',
            'description': 'Task description',
            'task_type': 'W'
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_task_type(self):
        data = {
            'name': 'Invalid Task',
            'task_type': 'X'  # Invalid choice
        }
        serializer = TaskCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('task_type', serializer.errors)

class TaskAssignSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='assign_test_user')

    def test_valid_assignment(self):
        data = {'user_ids': [self.user.id]}
        serializer = TaskAssignSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_empty_assignment(self):
        data = {'user_ids': []}
        serializer = TaskAssignSerializer(data=data)
        self.assertTrue(serializer.is_valid())  # Allowing empty is a design choice

    def test_invalid_user_ids(self):
        invalid_cases = [
            {'user_ids': ['not_an_int']},  # Wrong type
            {'user_ids': [999]},           # Non-existent user
            {'user_ids': None},            # Null value
            {'user_ids': [self.user.id, 'invalid']}  # Mixed valid/invalid
        ]
        
        for case in invalid_cases:
            with self.subTest(data=case):
                serializer = TaskAssignSerializer(data=case)
                self.assertFalse(serializer.is_valid())
                self.assertIn('user_ids', serializer.errors)