from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


# Customer User model textending towards Django AbstractUser
class User(AbstractUser):
    # Role choices for the platform
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('declutter', 'Decluttering Seller'),
        ('external', 'External Store Seller'),
        ('admin', 'Admin'),
    )


    # Role field determines permissions and dashboard routing
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} ({self.role})"
        # Human-readable representation

        
















