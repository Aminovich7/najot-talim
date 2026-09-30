from rest_framework.permissions import BasePermission
from .models import CustomUser, Wallet

class IsOwnerprofile(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user