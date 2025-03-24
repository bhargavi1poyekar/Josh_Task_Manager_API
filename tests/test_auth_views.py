from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tasks.models import User
from django.utils import timezone

class AuthViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User' 
            
        )
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User' 

        }
        response = self.client.post(url, data)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_missing_name_fields(self):
        url = reverse('user-register')
        invalid_data = {
            'username': 'incomplete',
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
            'email': 'incomplete@test.com'
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_username(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',  # Already exists
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'first_name': 'Existing',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_jwt_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)