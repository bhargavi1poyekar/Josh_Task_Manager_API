from rest_framework import serializers
from .models import Task
from users.models import User
from users.serializers import UserSerializer
from typing import List, Dict, Any


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying Task details with assigned users.
    """
    assigned_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                 'completed_at', 'status', 'assigned_users']

class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new tasks with validation.
    
    Validates:
    - Task type matches available choices
    - Name length (100 chars max)
    """
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type']
        extra_kwargs = {
            'name': {
                'max_length': 100
            },
            'task_type': {
                'help_text': "Task category: P (Personal), C (College), "
                             "W (Work), O (Other)"
            }
        }
    
    def validate_task_type(self, value: str) -> str:
        """Ensure task type is a valid choice"""
        valid_types = dict(Task.TaskType.choices).keys()
        if value not in valid_types:
            raise serializers.ValidationError(
                f"Invalid task type. Valid options: {', '.join(valid_types)}"
            )
        return value

class TaskAssignSerializer(serializers.Serializer):
    """
    Serializer for assigning users to tasks.
    
    Validates that all specified user IDs exist in the system.
    """

    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_user_ids(self, value: List[int]) -> List[int]:
        """
        Validate that all user IDs correspond to existing users.
        Args:
            value: List of user IDs to validate   
        Returns:
            Validated list of user IDs
        Raises:
            ValidationError: If any user IDs are invalid
        """
        existing_users = User.objects.filter(id__in=value)
        existing_ids = set(existing_users.values_list('id', flat=True))
        missing_ids = set(value) - existing_ids
        
        if missing_ids:
            raise serializers.ValidationError(
                f"User IDs not found: {sorted(missing_ids)}"
            )
            
        return value