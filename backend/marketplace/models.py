from django.db import models
from django.conf import settings

# Represents a shared marketplace category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    # Helps with admin readability
    def __str__(self):
        return self.name
    

class Product(models.Model):
    # Reference to the user who is selling the product
    # If the user is deleted, all their products will also be deleted
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )

    # Determines if admin has approved the product
    is_approved = models.BooleanField(default=False)

    # Name of the product (maximum of 255 characters)
    name = models.CharField(max_length=255)
    
    # Detailed description of the product
    description = models.TextField()

    # Price of the product (up to 10 digits total, 2 decimal places)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Available stock quantity (cannot be negative)
    stock = models.PositiveIntegerField(default=0)

    # Category of the product
    # If the category is deleted, this field will be set to NULL
    # It is optional (can be blank or null)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Determines if the product is active/visible in listings
    is_active = models.BooleanField(default=True)
    
    # Automatically stores the date and time when the product was created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the product (used in admin and shell)
    def __str__(self):
        return self.name
    


class Service(models.Model):
    # Reference to the user who provides the service
    # If the user is deleted, all their services will also be deleted
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services'
    )

    # Determines if admin has approved the product
    is_approved = models.BooleanField(default=False)

    # Title/name of the service (maximum of 255 characters)
    title = models.CharField(max_length=255)
    
    # Detailed description of the service
    description = models.TextField()

    # Base price for the service
    base_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Category of the service
    # If deleted, it will be set to NULL
    # This field is optional
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Determines if the service is currently available for booking/purchase
    is_available = models.BooleanField(default=True)
    
    # Automatically stores the date and time when the service was created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the service (used in admin and shell)
    def __str__(self):
        return self.title
