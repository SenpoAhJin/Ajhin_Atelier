from django.urls import path
from .views import ExternalSellerDashboard


urlpatterns = [
path("dashboard/", ExternalSellerDashboard.as_view()),











]