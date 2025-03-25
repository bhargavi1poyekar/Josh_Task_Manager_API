from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from typing import Dict, Any
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext as _

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes User model data
    
    Includes:
    - Read-only username
    - Calculated name property
    - Basic user information
    """
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile']
        extra_kwargs = {
            'username': {'read_only': True}
        }
    
    def get_name(self, obj: User) -> str:
        """Return combined first and last name"""
        return obj.name

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles user registration with password validation
    
    Features:
    - Password confirmation
    - Email/mobile uniqueness checks
    - Strong password validation
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 
            'password', 
            'password2',
            'email', 
            'first_name', 
            'last_name', 
            'mobile'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Main validation entry point"""
        self._validate_passwords(attrs)
        self._validate_unique_email(attrs.get('email'))
        self._validate_unique_mobile(attrs.get('mobile'))
        return attrs

    def _validate_passwords(self, attrs: Dict[str, Any]) -> None:
        """Validate password strength and match"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': _("Passwords do not match")
            })
        
        try:
            validate_password(attrs['password'])
        except DjangoValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
    

    def _validate_unique_email(self, email: str) -> None:
        """Ensure email uniqueness"""
        if email and User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                'email': _("This email is already registered")
            })

    def _validate_unique_mobile(self, mobile: str) -> None:
        """Ensure mobile uniqueness"""
        if mobile and User.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError({
                'mobile': _("This mobile number is already registered")
            })
    
    def create(self, validated_data: Dict[str, Any]) -> User:
        """Create user with proper password handling"""
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer
    
    Features:
    - Additional user data in response
    - Custom token claims
    - Active user validation
    """

    @classmethod
    def get_token(cls, user: User) -> Dict:
        """Add custom claims to JWT token"""
        token = super().get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['mobile'] = user.mobile
        return token


    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Add user data to token response"""
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data.update({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': self.user.id,
                'name': self.user.name,
                'email': self.user.email,
                'username': self.user.username
            }
        })

        return data