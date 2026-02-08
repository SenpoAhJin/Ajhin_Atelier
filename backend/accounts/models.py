# Model for external seller store profile
from django.conf import settings
from django.db import models

class ExternalStore(models.Model):
    # One external store per user
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    # Public store information
    store_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.store_name