from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

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

        
# Order model representing purchases or service commissions
class Order(models.Model):
    # Order status choices for tracking progress
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )


    # Customer who owns the order
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )


    # Current status of the order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    # Timestamp fields / Tracking of order time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    













# Create your models here.
