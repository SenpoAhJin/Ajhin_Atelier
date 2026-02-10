from django.urls import path
from .views import ExternalSellerDashboard
from django.urls import path
from .views import (
    CreateStoreProfileView,
    MyStoreProfileView,
    CreatePortfolioItemView,
    ListMyPortfolioView,
    CreateStoreListingView,
    ListMyListingsView,
    PublicStoreListingsView,
    CreateCommissionRequestView,
    ListIncomingCommissionsView,
    UpdateCommissionStatusView,
)


urlpatterns = [
path("dashboard/", ExternalSellerDashboard.as_view()),


# Store profile
path('profile/create/', CreateStoreProfileView.as_view()),
path('profile/me/', MyStoreProfileView.as_view()),

# Portfolio
path('portfolio/create/', CreatePortfolioItemView.as_view()),
path('portfolio/me/', ListMyPortfolioView.as_view()),

# Listings
path('listings/create/', CreateStoreListingView.as_view()),
path('listings/me/', ListMyListingsView.as_view()),
path('listings/store/<int:store_id>/', PublicStoreListingsView.as_view()),

# Commissions
path('commissions/create/<int:store_id>/', CreateCommissionRequestView.as_view()),
path('commissions/incoming/', ListIncomingCommissionsView.as_view()),
path('commissions/update/<int:commission_id>/', UpdateCommissionStatusView.as_view()),


]