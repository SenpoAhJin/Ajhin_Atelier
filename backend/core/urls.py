from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, DashboardView


urlpatterns = [
# Registration endpoint
path('register/', RegisterView.as_view()),


# JWT login endpoint
path('login/', TokenObtainPairView.as_view()),


# Token refresh endpoint
path('refresh/', TokenRefreshView.as_view()),


# Role-protected dashboard
path('dashboard/', DashboardView.as_view()),
]