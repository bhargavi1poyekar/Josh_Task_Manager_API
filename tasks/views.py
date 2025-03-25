from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.db import transaction
from .serializers import TaskSerializer, TaskCreateSerializer, TaskAssignSerializer
from users.serializers import UserSerializer, UserRegistrationSerializer
from users.models import User


class TaskCreateView(generics.CreateAPIView):
    """
    API endpoint that allows authenticated users to create new tasks.
    
    Method:POST

    Required Fields:
    - name: string (max 100 chars)
    - task_type: string (P/C/W/O)
    
    Returns:
    - 201 Created: Task created successfully
    - 400 Bad Request: Invalid input data
    - 401 Unauthorized: Authentication required
    """
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        """
        Save the task
        """
        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            raise ValidationError(
                {'database_error': str(e)},
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        """
        Exception handling for consistent error responses
        """
        if isinstance(exc, (ValidationError, NotFound)):
            return Response(
                {'error': str(exc)},
                status=exc.status_code
            )
        return super().handle_exception(exc)


class TaskAssignView(generics.GenericAPIView):
    """
    API endpoint for assigning users to a specific task
    
    Method:POST

    Required Fields:
    - List of user IDs in request body

    Returns:
    - Returns 200 OK on success
    - Returns 404 Not Found if task or users don't exist
    - Returns 403 Forbidden if user lacks permission
    """

    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskAssignSerializer

    def get_object(self):
        """
        Get task with existence check
        """
        try:
            task = super().get_object()
            return task
        except Task.DoesNotExist:
            raise NotFound("Task not found")

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                task = self.get_object()
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                
                user_ids = serializer.validated_data['user_ids']
                users = User.objects.filter(id__in=user_ids)

                # Validate all users exist
                if len(users) != len(user_ids):
                    missing_ids = set(user_ids) - set(users.values_list('id', flat=True))
                    raise ValidationError(
                        {'missing_users': list(missing_ids)},
                        code=status.HTTP_404_NOT_FOUND
                    )
        
                task.assigned_users.add(*users)
                
                return Response(
                    {
                        'status': 'success',
                        'assigned_users': list(users.values_list('id', flat=True)),
                        'task_id': task.id
                    },
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=getattr(e, 'status_code', status.HTTP_400_BAD_REQUEST)
            )
        

class UserTasksView(generics.ListAPIView):
    """
    API endpoint that returns tasks assigned to a specific user
    
    Returns:
    - 200 OK: List of tasks
    - 404 Not Found: If requested user doesn't exist
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer


    def get_queryset(self):
        """Get validated queryset"""
        user_id = self.kwargs['user_id']

        # Validate user exists
        if not User.objects.filter(id=user_id).exists():
            raise NotFound(f"User {user_id} not found")
        
        return Task.objects.filter(assigned_users__id=user_id)

