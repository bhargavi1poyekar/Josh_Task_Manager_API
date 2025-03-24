from django.db import models
from django.conf import settings

class Task(models.Model):

    TASK_TYPES = (
        ('P', 'Personal'),
        ('C', 'College'),
        ('W', 'Work'),
        ('O', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('C', 'Completed'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=1, choices=TASK_TYPES, default='O')
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    assigned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')
    
    def __str__(self):
        return self.name