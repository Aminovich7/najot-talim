from rest_framework.permissions import BasePermission, SAFE_METHODS


# admin ham delete qila oladi bloglarni, ohirida qilganim uchun class nomini ozgartirmadim(class IsAuthorOrReadOnly)
class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_staff or request.user.role == "author"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author == request.user


class IsUserOrAdminForComment(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.is_staff or request.user.role == "author"

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author == request.user
