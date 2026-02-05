from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

class HealthCheck(APIView):
    def get(self, request):
        return Response({"status": "ok"})
    

# User registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT tokens for the new users
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

