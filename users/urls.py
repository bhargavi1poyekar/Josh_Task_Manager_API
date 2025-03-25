from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, UserRegistrationView


urlpatterns = [
    # POST - Obtain JWT access and refresh tokens
    # Body: { username, password }
    # Returns: { access, refresh }
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # POST - Refresh JWT access token using refresh token
    # Body: { refresh }
    # Returns: { access }
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # POST - Register a new user
    # Body: { username, password, email, etc. }
    # Returns: User details or success message
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]