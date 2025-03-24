from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'mobile']
        extra_kwargs = {
            'username': {'read_only': True}
        }
    
    def get_name(self, obj):
        return obj.name

class UserRegistrationSerializer(serializers.ModelSerializer):
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
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        # Remove password2 from validated_data
        validated_data.pop('password2')
        
        user = User.objects.create_user(
            **validated_data
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['mobile'] = user.mobile
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] = {
            'id': self.user.id,
            'name': self.user.name,
            'email': self.user.email
        }
        
        return data