from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .auth_views import (
    CustomTokenObtainPairView,
    UserRegistrationView
)

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
]