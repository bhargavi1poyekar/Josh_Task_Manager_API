from rest_framework import serializers
from .models import Task
from users.models import User
from users.serializers import UserSerializer

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                 'completed_at', 'status', 'assigned_users']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type']

class TaskAssignSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_user_ids(self, value):
        # Check all user IDs exist
        existing_ids = set(User.objects.filter(
            id__in=value
        ).values_list('id', flat=True))
        
        missing_ids = set(value) - existing_ids
        if missing_ids:
            raise serializers.ValidationError(
                f"Users not found: {sorted(missing_ids)}"
            )
        return value