from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response # Important Response Action
from rest_framework.views import APIView # Allowings request to the database
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Order, DeclutterItem
from .serializers import OrderSerializer, AccountSerializer, DeclutterItemSerializer

class HealthCheck(APIView):
    def get(self, request):
        return Response({"status": "ok"})
    

# User registration endpoint
class RegisterView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
           user = serializer.save()


           # Generate JWT tokens for the new user
           refresh = RefreshToken.for_user(user)


           return Response({
            'user': user.username,
            'role': user.role,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=400)

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


# Public marketplace view for declutter items
class DeclutterMarketplaceView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Fetch only active listings
        items = DeclutterItem.objects.filter(is_active=True)
        serializer = DeclutterItemSerializer(items, many=True)
        return Response(serializer.data)
    

# Seller dashboard view for managing own declutter items
class SellerDeclutterDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch only listings created by the logged-in seller
        items = DeclutterItem.objects.filter(seller=request.user)
        serializer = DeclutterItemSerializer(
            data = request.data,
            context = {'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)