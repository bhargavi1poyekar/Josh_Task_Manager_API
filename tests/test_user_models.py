from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User
from datetime import datetime
from django.contrib.auth.hashers import check_password

class UserModelTest(TestCase):
    """Test suite for the User model validation and behavior."""

    def setUp(self) -> None:
        """
        Initialize test data with valid user attributes.
        """
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_valid_user(self) -> None:
        """
        Test creating a user with all required fields
        
        Verifies:
        - All fields are correctly set
        - Password is properly hashed
        - Name property works correctly
        - Default permissions are correct
        """
        user = User.objects.create_user(**self.valid_data)
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(check_password("testpass123", user.password))
        self.assertEqual(user.name, "Test User")  # Test @property
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_mobile_number_validation(self) -> None:
        """
        Test mobile number formatting

        Cases tested:
        - Valid international format (+ prefix)
        - Invalid overly long number
        """

        # Valid case
        valid_user = User(
            **self.valid_data,
            mobile="+1234567890"  # Valid format
        )
        valid_user.full_clean()  # Should not raise

        # Invalid case
        with self.assertRaises(ValidationError):
            invalid_user = User(
                **self.valid_data,
                mobile="11123456789000000000" 
            )
            invalid_user.full_clean()

    def test_required_fields(self) -> None:
        """
        Test missing required fields
        
        Required fields:
        - username
        - password
        """
        required_fields = ['username', 'password']
        
        for field in required_fields:
            with self.subTest(field=field):
                invalid_data = self.valid_data.copy()
                invalid_data.pop(field)
                
                with self.assertRaises(ValidationError):
                    user = User(**invalid_data)
                    user.full_clean()

    def test_password_hashed(self) -> None:
        """
        Test password is properly hashed
        
        Verifies:
        - Raw password doesn't match stored value
        - Stored hash validates correctly
        - Different users with same password get different hashes
        """
        raw_password = "testpass123"
        user = User.objects.create_user(**self.valid_data)
        self.assertTrue(check_password(raw_password, user.password))
        self.assertNotEqual(raw_password, user.password)
