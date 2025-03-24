from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import User, Task
from django.utils import timezone

class TaskViewTests(APITestCase):
    def setUp(self):
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

    def test_create_task(self):
        url = reverse('task-create')
        data = {
            'name': 'API Task',
            'description': 'Created via API',
            'task_type': 'W'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_assign_task(self):
        url = reverse('task-assign', kwargs={'pk': self.task.id})
        data = {
            'user_ids': [self.other_user.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.task.assigned_users.count(), 2)

    def test_get_user_tasks(self):
        url = reverse('user-tasks', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Task')


class PermissionTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.task = Task.objects.create(name='Private Task', status='P')
        self.task.assigned_users.add(self.user1)

    def test_unauthenticated_access(self):
        urls = [
            reverse('task-create'),
            reverse('user-tasks', kwargs={'user_id': 1})
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_task_access(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(
            reverse('user-tasks', kwargs={'user_id': self.user1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class EdgeCaseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='edgeuser', password='edgepass')
        self.client.force_authenticate(user=self.user)

    def test_create_invalid_task(self):
        url = reverse('task-create')
        invalid_data = [
            {'description': 'Missing name'},  # No name
            {'name': 'X', 'task_type': 'Invalid'},  # Invalid task type
            {}  # Empty data
        ]
        
        for data in invalid_data:
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_nonexistent_user(self):
        task = Task.objects.create(name='Edge Task')
        url = reverse('task-assign', kwargs={'pk': task.id})
        
        # Test with clearly non-existent ID
        response = self.client.post(url, {'user_ids': [99999]}, format='json')
        
        # Should return 404
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify error message contains the missing ID
        self.assertIn('99999', str(response.data))
        
        # Verify no assignments were made
        self.assertEqual(task.assigned_users.count(), 0)