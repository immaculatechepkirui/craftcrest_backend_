from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "user_type", None) == "ADMIN":
            return True
        return getattr(obj, "artisan", None) == request.user