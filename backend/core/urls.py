from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, DashboardView
from .views import(
    CustomerOverviewView,
    OrderHistoryView,
    AccountSettingsView,
    MessagingPlaceholderView,
)


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



urlpatterns += [
    # Customer dashboard endpoints
    path('dashboard/overview/', CustomerOverviewView.as_view()),
    path('dashboard/orders/', OrderHistoryView.as_view()),
    path('dashboard/account/', AccountSettingsView.as_view()),
    path('dashboard/messages/', MessagingPlaceholderView.as_view()),
]