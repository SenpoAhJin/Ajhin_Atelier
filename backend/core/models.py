from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from marketplace.models import Category

# Customer User model textending towards Django AbstractUser
class User(AbstractUser):
    # Role choices for the platform
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('declutter_seller', 'Decluttering Seller'),
        ('external_seller', 'External Store Seller'),
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
    

# Model representing a casual, one-off cosplay item sale
# This class allows the users to sell their prev cosplays
class DeclutterItem(models.Model):
    # Condition choices for transparency
    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
    )


    # Seller who owns the listing
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='declutter_items'
    )

    # Basic item details
    title = models.CharField(max_length=255)
    description = models.TextField()

    # Item condition (new or used)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)

    # Quantity is limited by design (default 1)
    quantity = models.PositiveBigIntegerField(default=1)

    # Price of the item
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Availability flag
    is_active = models.BooleanField(default=True)

    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    def __str__(self):
        return f"{self.title} ({self.condition})" # Human readable identifier
    

