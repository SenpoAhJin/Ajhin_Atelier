from django.shortcuts import render
# External seller dashboard overview
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import ExternalStore


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
