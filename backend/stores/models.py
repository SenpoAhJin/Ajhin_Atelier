# Portfolio items showcase previous works
from django.db import models
from accounts.models import ExternalStore


class PortfolioItem(models.Model):
    store = models.ForeignKey(ExternalStore, on_delete=models.CASCADE, related_name="portfolio")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="portfolio/")
    description = models.TextField(blank=True)


    created_at = models.DateTimeField(auto_now_add=True)



# Store listings can be either product or service
class StoreListing(models.Model):
    LISTING_TYPE_CHOICES = (
    ("product", "Product"),
    ("service", "Service"),
    )


    store = models.ForeignKey(ExternalStore, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)