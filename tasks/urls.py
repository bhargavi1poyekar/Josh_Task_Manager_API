from django.urls import path
from .views import TaskCreateView, TaskAssignView, UserTasksView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/assign/', TaskAssignView.as_view(), name='task-assign'),
    path('users/<int:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
    
]