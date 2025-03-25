from django.test import TestCase
from rest_framework.exceptions import ValidationError
from tasks.models import Task
from users.models import User
from users.serializers import UserSerializer, UserRegistrationSerializer


class UserSerializerTest(TestCase):
    """Test suite for the UserSerializer output representation."""

    def setUp(self) -> None:
        """
        Set up test data for UserSerializer tests.
        Creates a test user with complete profile data.
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            mobile='+1234567890'
        )

    def test_serializer_output(self) -> None:
        """
        Test the serializer outputs the correct fields and data.
        
        Verifies:
        - All expected fields are present
        - Field order matches expectations
        - Computed properties (like 'name') work correctly
        - Sensitive fields (password) are excluded
        """
        serializer = UserSerializer(self.user)
        expected_fields = ['id', 'username', 'name', 'email', 'mobile']
        self.assertEqual(list(serializer.data.keys()), expected_fields)
        self.assertEqual(serializer.data['name'], 'Test User')


class UserRegistrationSerializerTest(TestCase):
    """Test suite for UserRegistrationSerializer validation rules."""

    def test_valid_registration(self) -> None:
        """
        Test successful registration with valid data.
        
        Valid cases:
        - All required fields present
        - Matching passwords
        - Valid email format
        - Strong password
        """
        data = {
            'username': 'newuser',
            'password': 'ValidPass123!',
            'password2': 'ValidPass123!',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self) -> None:
        """
        Test registration fails when passwords don't match.
        
        Verifies:
        - Validation fails
        """
        data = {
            'username': 'newuser',
            'password': 'ValidPass123!',
            'password2': 'Different123!',
            'email': 'new@example.com'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())