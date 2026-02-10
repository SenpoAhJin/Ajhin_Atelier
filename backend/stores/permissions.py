from rest_framework.permissions import BasePermission


class IsExternalSeller(BasePermission):
    """
    Allows access only to users with the external seller role.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # User must have external seller role
        return request.user.role == 'external_seller'


class IsStoreOwner(BasePermission):
    """
    Allows access only if the authenticated user owns the store.
    """

    def has_object_permission(self, request, view, obj):
        # The store owner must match the authenticated user
        return obj.owner == request.user
