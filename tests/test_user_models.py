from django.test import TestCase
from django.core.exceptions import ValidationError
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
