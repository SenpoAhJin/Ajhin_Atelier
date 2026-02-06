from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.response import Response # Important Response Action
from rest_framework.views import APIView # Allowings request to the database
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Order
from .serializers import OrderSerializer, AccountSerializer

class HealthCheck(APIView):
    def get(self, request):
        return Response({"status": "ok"})
    

    

# Dashboard overview 
class DashboardView(APIView):
    def get(self, request):

        # returns role-based dashboard data
        return Response({
            'username': request.user.username,
            'role': request.user.role,
            'message': f"Welcome to the {request.user.role} dashboard"
        })


# Overview dashboard endpoint
class CustomerOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Query only orders belonging to the logged-in user
        orders = Order.objects.filter(customer=request.user)

        # Aggregate counts for the dashboard summary
        return Response({
            'total_orders': orders.count(),
            'pending_orders': orders.filter(status='pending').count(),
            'completed_orders': orders.filter(status='completed').count(),
        })
    

# Order history endpoint
class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Securely fetch only the user's orders
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')


        # Handle empty state automatically
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

# Account settings endpoint
class AccountSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #Serialize current user's account info
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)
    

# Messaging placeholder endpoint
class MessagingPlaceholderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Placeholder response for future messaging feature that we will implement
        return Response({
            'message': 'Messaging system coming soon...'
        })
