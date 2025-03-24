from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    mobile = models.CharField(max_length=10, blank=True, null=True)
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.name or self.username