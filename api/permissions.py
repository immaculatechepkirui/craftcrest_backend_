from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Allow access to object owners or admins.
    Adjust the admin check to match your project (here we check user.user_type == "ADMIN").
    """
    def has_object_permission(self, request, view, obj):
        if getattr(request.user, "user_type", None) == "ADMIN":
            return True
        return getattr(obj, "artisan", None) == request.user

