from django.urls import path
from .views import MarketplaceListView

urlpatterns = [
    path("", MarketplaceListView.as_view(), name="marketplace-list"),
]
