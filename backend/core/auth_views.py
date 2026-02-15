from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        user = User.objects.filter(username=username).first()

        # 🔒 Check lock BEFORE auth
        if user and user.is_locked():
            return Response(
                {"detail": "Account temporarily locked. Try again later."},
                status=status.HTTP_403_FORBIDDEN
            )

        response = super().post(request, *args, **kwargs)

        # ❌ Failed login
        if response.status_code == 401 and user:
            user.register_failed_attempt()

        # ✅ Successful login
        if response.status_code == 200 and user:
            user.reset_login_attempts()

        return response
