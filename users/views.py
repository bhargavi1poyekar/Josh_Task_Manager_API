from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API endpoint to obtain JWT tokens (access and refresh).
    
    Method: POST

    Required Fields:
    - username: string
    - password: string
    
    Returns:
    - 200 OK: Returns access and refresh tokens
    - 401 Unauthorized: Invalid credentials
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint to register a new user.
    
    Method: POST

    Required Fields:
    - username: string (unique)
    - email: string (valid email format)
    
    Returns:
    - 201 Created: User registered successfully
    - 400 Bad Request: Invalid input data
    - 500 Internal Server Error: Unexpected error
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer) -> None:
        """
        Handles user creation and securely sets the password.

        Method: Internal

        Args:
        - serializer: Validated user data from request

        Raises:
        - ValidationError: If password is invalid or data is incomplete
        - Exception: For any unexpected error during user creation
        """
        try:
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')

            # Check for missing or invalid fields
            if not username:
                raise ValidationError({"username": "Username is required."})
            if not email:
                raise ValidationError({"email": "Email is required."})
            if not password:
                raise ValidationError({"Password": "Password is required."})
            
            instance = serializer.save()
            instance.set_password(serializer.validated_data['password'])
            instance.save()

        except ValidationError as e:
            raise ValidationError(
                {
                    "error": e.detail if isinstance(e.detail, dict) else str(e),
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )

        except Exception as e:
            raise ValidationError(
                {
                    "error": f"An unexpected error occurred: {str(e)}",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                }
            )