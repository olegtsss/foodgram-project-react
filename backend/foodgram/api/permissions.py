from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff)


class AdminOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Этот метод нужен, иначе может провалиться второй метод
        return (
            request.method in SAFE_METHODS or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or obj.author == request.user)
