from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
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
    
    def test_password_mismatch(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'password': 'password123',
            'password2': 'differentpassword',  # Doesn't match
            'email': 'new@example.com',
            'first_name': 'password',
            'last_name': 'mismatch'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_jwt_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_login_nonexistent_user(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'nouser',  
            'password': 'anypassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_wrong_password(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'existinguser',
            'password': 'wrongpassword'  # Incorrect
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_anon_throttling_for_registration(self):
        """Test that anonymous users are throttled for registration attempts."""
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'password2': 'newpass123',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User' 

        }
        # anon limit is 50/hour. 
        for _ in range(50):
            response = self.client.post(url, data)
            self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
        
        # 51st request should be throttled
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)