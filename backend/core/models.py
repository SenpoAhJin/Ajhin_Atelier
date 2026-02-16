from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from marketplace.models import Category
from django.utils import timezone
from datetime import timedelta


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

    failed_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(null=True, blank=True)
    lock_level = models.IntegerField(default=0)  # 0,1,2 (progressive)

    def is_locked(self):
        if self.lock_until and timezone.now() < self.lock_until:
            return True
        return False

    def register_failed_attempt(self):
        self.failed_attempts += 1

        if self.failed_attempts >= 5:
            self.lock_level += 1
            self.failed_attempts = 0

            if self.lock_level == 1:
                lock_minutes = 5
            elif self.lock_level == 2:
                lock_minutes = 10
            else:
                lock_minutes = 30

            self.lock_until = timezone.now() + timedelta(minutes=lock_minutes)

        self.save()

    def reset_login_attempts(self):
        self.failed_attempts = 0
        self.lock_level = 0
        self.lock_until = None
        self.save()

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
        related_name='core_orders'
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
    
    # Determines if admin has approved the listing
    is_approved = models.BooleanField(default=False)


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
    

