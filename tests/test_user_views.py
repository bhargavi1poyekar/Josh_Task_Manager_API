from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import User
from django.utils import timezone
from django.test import override_settings

class AuthViewTests(APITestCase):
    """Test suite for authentication-related API endpoints."""

    # Overriding the rate limitng for testcases. 
    @override_settings(REST_FRAMEWORK={
        'DEFAULT_THROTTLE_CLASSES': [],
        'DEFAULT_THROTTLE_RATES': {}
    })
    

    def setUp(self) -> None:
        """
        Initialize test data.
        Creates a test user and API client for authentication tests.
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            first_name='Test',
            last_name='User' 
            
        )
        self.client = APIClient()

    def test_user_registration(self) -> None:
        """
        Test successful user registration.

        Verifies:
        - correct status code 
        - user creation in database.
        """
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_missing_name_fields(self) -> None:
        """
        Test registration with missing name fields.

        Verifies:
        - return 400 Bad Request.
        """
        url = reverse('user-register')
        invalid_data = {
            'username': 'incomplete',
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
            'email': 'incomplete@test.com'
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_username(self) -> None:
        """
        Test registration with existing username.

        Verifies:
        - return 400 with username error.
        """
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
    
    def test_password_mismatch(self) -> None:
        """
        Test registration with mismatched passwords.

        Verifies:
        - return 400 Bad Request.
        """
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
    
    def test_jwt_login(self) -> None:
        """
        Test successful JWT token obtainment.
        
        Verifies 
        - 200 status code
        - access token in response.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_login_nonexistent_user(self) -> None:
        """
        Test login with non-existent user.
        
        Verifies:
        - return 401 Unauthorized.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'nouser',  
            'password': 'anypassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_wrong_password(self) -> None:
        """
        Test login with incorrect password.
        
        Verifies:
        - return 401 Unauthorized.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'existinguser',
            'password': 'wrongpassword'  # Incorrect
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)