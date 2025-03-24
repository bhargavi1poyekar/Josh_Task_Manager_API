from django.test import TestCase
from rest_framework.exceptions import ValidationError
from tasks.models import User, Task
from tasks.auth_serializers import (
    UserSerializer,
    UserRegistrationSerializer
)


class UserSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            mobile='1234567890'
        )

    def test_serializer_output(self):
        serializer = UserSerializer(self.user)
        expected_fields = ['id', 'username', 'name', 'email', 'mobile']
        self.assertEqual(list(serializer.data.keys()), expected_fields)
        self.assertEqual(serializer.data['name'], 'Test User')

class UserRegistrationSerializerTest(TestCase):
    def test_valid_registration(self):
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

    def test_password_mismatch(self):
        data = {
            'username': 'newuser',
            'password': 'ValidPass123!',
            'password2': 'Different123!',
            'email': 'new@example.com'
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())