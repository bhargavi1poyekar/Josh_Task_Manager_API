from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds mobile number field and name property.
    
    Attributes:
        mobile (str): User's mobile phone number (optional)
        name (property): Combined first and last name
    """

    MOBILE_MAX_LENGTH = 15
    NAME_MAX_LENGTH = 150

    # Phone number validation regex
    PHONE_REGEX = RegexValidator(
        regex=r'^\+?1?\d{9,15}$'
    )

    # Custom fields
    mobile = models.CharField(
        max_length=MOBILE_MAX_LENGTH,
        validators=[PHONE_REGEX],
        blank=True,
        null=True,
        unique=True,
    )
    
    @property
    def name(self) -> str:
        """Combined name property (first + last names)"""
        return f"{self.first_name} {self.last_name}".strip()

    class Meta(AbstractUser.Meta):
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
        # Prevent clashes with default User model
        swappable = 'AUTH_USER_MODEL'

    def __str__(self) -> str:
        """String representation for the user model"""
        return self.name or self.username