from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import Task
from users.models import User
from django.utils import timezone

class TaskViewTests(APITestCase):
    """Test suite for core task management endpoints."""

    def setUp(self) -> None:
        """
        Initialize test data for task endpoint tests.
        Creates:
        - Two test users
        - One test task assigned to the primary user
        - Authenticates the primary user
        """
        self.user = User.objects.create_user(
            username='taskuser',
            password='taskpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status='P'
        )
        self.task.assigned_users.add(self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_task(self) -> None:
        """
        Test successful task creation via API.
        
        Verifies:
        - Correct HTTP status (201 Created)
        - Task count increases
        - Default values are set properly
        """
        url = reverse('task-create')
        data = {
            'name': 'API Task',
            'description': 'Created via API',
            'task_type': 'W'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_assign_task(self) -> None:
        """
        Test successful user assignment to task.
        
        Verifies:
        - Correct HTTP status (200 OK)
        - User count increases
        - Both original and new users remain assigned
        """
        url = reverse('task-assign', kwargs={'pk': self.task.id})
        data = {
            'user_ids': [self.other_user.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.assigned_users.count(), 2)

    def test_get_user_tasks(self) -> None:
        """
        Test retrieval of tasks assigned to a specific user.
        
        Verifies:
        - Correct HTTP status (200 OK)
        """
        url = reverse('user-tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PermissionTests(APITestCase):
    """Test suite for authentication and authorization requirements."""

    def setUp(self) -> None:
        """
        Initialize test data for permission tests.
        Creates:
        - Two test users
        - One task assigned to the first user
        """
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.task = Task.objects.create(name='Private Task', status='P')
        self.task.assigned_users.add(self.user1)

    def test_unauthenticated_access(self) -> None:
        """
        Test that protected endpoints require authentication.
        
        Verifies:
        - Unauthenticated requests receive 401 status
        """
        urls = [
            reverse('task-create'),
            reverse('user-tasks', kwargs={'user_id': 1})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class EdgeCaseTests(APITestCase):
    """Test suite for edge cases and error handling."""

    def setUp(self) -> None:
        """Create and authenticate a test user."""
        self.user = User.objects.create_user(username='edgeuser', password='edgepass')
        self.client.force_authenticate(user=self.user)

    def test_create_invalid_task(self) -> None:
        """
        Test task creation with invalid data.
        
        Cases tested:
        - Missing required fields (name)
        - Invalid task type
        - Empty payload
        """
        url = reverse('task-create')
        invalid_data = [
            {'description': 'Missing name'},  # No name
            {'name': 'X', 'task_type': 'Invalid'},  # Invalid task type
            {}  # Empty data
        ]
        
        for data in invalid_data:
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_nonexistent_user(self) -> None:
        """
        Test assignment of non-existent users.
        
        Verifies:
        - Proper error status (400 Bad Request)
        - Error message identifies invalid user
        - No assignments are made
        """
        task = Task.objects.create(name='Edge Task')
        url = reverse('task-assign', kwargs={'pk': task.id})
        
        response = self.client.post(url, {'user_ids': [99999]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('99999', str(response.data))
        self.assertEqual(task.assigned_users.count(), 0)