from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, DashboardView
from .views import(
    CustomerOverviewView,
    OrderHistoryView,
    AccountSettingsView,
    MessagingPlaceholderView,
    DeclutterMarketplaceView,
    SellerDeclutterDashboardView,
    DeclutterItemDeactivateView,
    DeclutterContactSellerView,
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


# Decluttering Seller endpoint
path('declutter/my-items/', SellerDeclutterDashboardView.as_view(), name='seller-declutter-items'),
path('declutter/items/<int:item_id>/sold/', DeclutterItemDeactivateView.as_view(), name='declutter-item-sold'),
path('declutter/items/<int:item_id>/contact/', DeclutterContactSellerView.as_view(), name='declutter-contact-seller'),






]



urlpatterns += [
    # Customer dashboard endpoints
    path('dashboard/overview/', CustomerOverviewView.as_view()),
    path('dashboard/orders/', OrderHistoryView.as_view()),
    path('dashboard/account/', AccountSettingsView.as_view()),
    path('dashboard/messages/', MessagingPlaceholderView.as_view()),


    # Public declutting marketplace
    path('marketplace.declutter/', DeclutterMarketplaceView.as_view()),

    # Seller dashboard for declutter items
    path('seller/declutter/', SellerDeclutterDashboardView.as_view())
]