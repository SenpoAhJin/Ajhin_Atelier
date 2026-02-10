from django.shortcuts import render
# External seller dashboard overview
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import ExternalStore
from rest_framework import status
from .models import (
    StoreProfile,
    PortfolioItem,
    StoreListing,
    CommissionRequest
)

from .serializers import (
    StoreProfileSerializer,
    PortfolioItemSerializer,
    StoreListingSerializer,
    CommissionRequestSerializer
)
from .permissions import IsExternalSeller, IsStoreOwner



class ExternalSellerDashboard(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        # Ensure user is an external seller
        store = ExternalStore.objects.get(owner=request.user)


        return Response({
        "store_name": store.store_name,
        "active_listings": store.listings.count(),
        "portfolio_items": store.portfolio.count(),
        })

class CreateStoreProfileView(APIView):
    """
    External seller creates their store profile.
    One store per seller.
    """
    # Only authenticated users with the External Seller role can access this
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def post(self, request):
        # Prevent duplicate store creation for the same seller
        # Each external seller is allowed only ONE store profile
        if hasattr(request.user, 'store_profile'):
            return Response(
                {"detail": "Store profile already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate incoming store profile data
        serializer = StoreProfileSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically bind the store owner to the logged-in user
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return validation errors if input data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyStoreProfileView(APIView):
    """
    Retrieve the authenticated seller's store profile.
    """
    # Seller must be logged in and have external seller permissions
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def get(self, request):
        # Fetch the store profile linked to the current user
        store = request.user.store_profile
        serializer = StoreProfileSerializer(store)
        return Response(serializer.data)


class CreatePortfolioItemView(APIView):
    """
    Upload a new portfolio item
    """
    # Only external sellers can upload portfolio items
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def post(self, request):
        # Get the seller's store profile
        store = request.user.store_profile

        # Validate portfolio item input data
        serializer = PortfolioItemSerializer(data=request.data)

        if serializer.is_valid():
            # Associate the portfolio item with the seller's store
            serializer.save(store=store)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return validation errors if upload fails
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
    

class ListMyPortfolioView(APIView):
    """
    List all portfolio items of the seller
    """
    # Seller-only endpoint
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def get(self, request):
        # Fetch only portfolio items belonging to the seller's store
        items = PortfolioItem.objects.filter(store=request.user.store_profile)
        serializer = PortfolioItemSerializer(items, many=True)
        return Response(serializer.data)
    


class CreateStoreListingView(APIView):
    """
    Create a product or service listing.
    """
    # Only authenticated external sellers can create listings
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def post(self, request):
        # Get the seller's store profile
        store = request.user.store_profile

        # Validate listing input (product or service)
        serializer = StoreListingSerializer(data=request.data)

        if serializer.is_valid():
            # Bind listing to the seller's store
            serializer.save(store=store)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return errors if listing data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMyListingsView(APIView):
    """
    List all listings created by the seller.
    """
    # Seller-only access
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def get(self, request):
        # Fetch all listings owned by the seller
        listings = StoreListing.objects.filter(store=request.user.store_profile)
        serializer = StoreListingSerializer(listings, many=True)
        return Response(serializer.data)


class PublicStoreListingsView(APIView):
    """
    Public endpoint to view listings of a store.
    """
    def get(self, request, store_id):
        # Fetch only ACTIVE listings for a specific store
        listings = StoreListing.objects.filter(
            store_id=store_id,
            is_active=True
        )
        serializer = StoreListingSerializer(listings, many=True)
        return Response(serializer.data)


class CreateCommissionRequestView(APIView):
    """
    Customer submits a commission request to a store.
    """
    # Any authenticated user (customer) can submit a commission request
    permission_classes = [IsAuthenticated]

    def post(self, request, store_id):
        # Identify which store the commission is sent to
        store = StoreProfile.objects.get(id=store_id)

        # Validate commission request input
        serializer = CommissionRequestSerializer(data=request.data)

        if serializer.is_valid():
            # Bind commission request to the customer and target store
            serializer.save(
                customer=request.user,
                store=store
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListIncomingCommissionsView(APIView):
    """
    External seller views incoming commission requests.
    """
    # Only external sellers can view commissions sent to their store
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def get(self, request):
        # Fetch commission requests addressed to the seller's store
        commissions = CommissionRequest.objects.filter(
            store=request.user.store_profile
        )
        serializer = CommissionRequestSerializer(commissions, many=True)
        return Response(serializer.data)


class UpdateCommissionStatusView(APIView):
    """
    External seller updates commission status and quoted price.
    """
    # Seller-only permission
    permission_classes = [IsAuthenticated, IsExternalSeller]

    def patch(self, request, commission_id):
        # Fetch the commission request owned by the seller's store
        commission = CommissionRequest.objects.get(
            id=commission_id,
            store=request.user.store_profile
        )

        # Seller controls quote & status updates
        # Partial update allowed (PATCH)
        commission.quoted_price = request.data.get(
            'quoted_price',
            commission.quoted_price
        )
        commission.status = request.data.get(
            'status',
            commission.status
        )
        commission.save()

        # Return updated commission data
        serializer = CommissionRequestSerializer(commission)
        return Response(serializer.data)
