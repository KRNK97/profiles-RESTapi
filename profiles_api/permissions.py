from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit own profile"""

    def has_object_permission(self, request, view, obj):
        """check user is trying to edit own profile"""
        # we allow any user to view any profile which will be "GET" request, and it is considered a safe request
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.id == obj.id:   # if it is same user then true
                return True
            else:
                return False
