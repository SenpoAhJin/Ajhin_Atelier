from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer




class CustomLoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        # 🔐 Check if account is locked
        if user_obj.is_locked():
            remaining = (user_obj.lock_until - timezone.now()).seconds // 60
            return Response(
                {"error": f"Account locked. Try again in {remaining} minutes."},
                status=403
            )

        user = authenticate(username=username, password=password)

        if user is None:
            user_obj.register_failed_attempt()
            return Response({"error": "Invalid credentials"}, status=400)

        # ✅ Successful login
        user.reset_login_attempts()

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "role": user.role,
        })






