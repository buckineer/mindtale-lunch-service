from typing import Optional

from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from lunch_service.restaurant.models import Restaurant

from .models import UserRole


class IsCompanyAdmin(permissions.IsAuthenticated):
    def has_permission(self, request: Request, view) -> bool:
        if not super().has_permission(request, view):
            return False

        # Assert that request.user is not AnonymousUser for the type checker
        assert not isinstance(request.user, AnonymousUser), "request.user is AnonymousUser"
        return request.user.role == UserRole.ADMIN


class IsRestaurant(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        api_key: Optional[str] = request.headers.get('API-Key')
        if not api_key:
            return False

        try:
            restaurant: Restaurant = Restaurant.objects.get(api_key=api_key)
            # Dynamically adding an attribute to request. Type checkers won't like this without stubs or extensions.
            request.restaurant = restaurant  # type: ignore
            return True
        except Restaurant.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')


class IsEmployee(permissions.IsAuthenticated):

    def has_permission(self, request: Request, view) -> bool:
        if not super().has_permission(request, view):
            return False

        # Assert that request.user is not AnonymousUser for the type checker
        assert not isinstance(request.user, AnonymousUser), "request.user is AnonymousUser"
        return request.user.role == UserRole.EMPLOYEE
