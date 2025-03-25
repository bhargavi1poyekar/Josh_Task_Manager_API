from django.urls import path
from .views import TaskCreateView, TaskAssignView, UserTasksView
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    # POST - Create new task
    # Body: { name, description, task_type }
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),

    # POST - Assign users to a specific task
    # Parameters: pk (Task ID)
    # Body: { user_ids: [<user_id1>, <user_id2>...] }
    path('tasks/<int:pk>/assign/', TaskAssignView.as_view(), name='task-assign'),

    # GET - Retrieve tasks assigned to a specific user
    # Parameters: user_id (User ID)
    # Returns: List of tasks with details
    path('users/<int:user_id>/tasks/', UserTasksView.as_view(), name='user-tasks'),
]