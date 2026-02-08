# Permission for external sellers only
from rest_framework.permissions import BasePermission


class IsExternalSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "external_seller"