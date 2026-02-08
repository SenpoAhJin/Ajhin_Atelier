# Custom commission request from client to seller
from django.conf import settings
from django.db import models
from stores.models import StoreListing


class CommissionRequest(models.Model):
    STATUS_CHOICES = (
    ("pending", "Pending"),
    ("quoted", "Quoted"),
    ("accepted", "Accepted"),
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
    )


    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(StoreListing, on_delete=models.CASCADE)
    description = models.TextField()
    quoted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")


    created_at = models.DateTimeField(auto_now_add=True)