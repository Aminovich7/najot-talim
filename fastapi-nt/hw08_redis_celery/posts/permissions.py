from .models import Post, Comment
from users.models import CustomUser
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return  request.user.is_authenticated and request.user.is_staff
    
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        request.user.is_authenticated and request.user == obj.author

class IsPremiumUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.is_premium:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.is_premium_active