from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsActiveEmployee(permissions.BasePermission):
    """
    Custom permission to only allow active employees to access the API.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.user and request.user.is_active and request.user.is_staff
        )
