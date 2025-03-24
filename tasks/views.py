from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Task, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializers import (TaskSerializer, TaskCreateSerializer, 
                         TaskAssignSerializer, UserSerializer, UserRegistrationSerializer)

class TaskCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save()

class TaskAssignView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskAssignSerializer

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_ids = serializer.validated_data['user_ids']
        users = User.objects.filter(id__in=user_ids)

        # Validate all users exist
        if len(users) != len(user_ids):
            missing_ids = set(user_ids) - set(users.values_list('id', flat=True))
            raise NotFound(f"Users not found: {missing_ids}")
        
        task.assigned_users.add(*users)
        
        return Response(
            {'status': 'Users assigned successfully'},
            status=status.HTTP_200_OK
        )

class UserTasksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Task.objects.filter(assigned_users__id=user_id)

