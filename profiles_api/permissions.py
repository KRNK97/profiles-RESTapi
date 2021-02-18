from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit own profile"""

    def has_object_permission(self, request, view, obj):
        """check user is trying to edit own profile"""
        # we allow any user to view any profile which will be "GET" request, and it is considered a safe request
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # after auth login, we will get loggedin user with the request
            if request.user.id == obj.id:   # if it is same as object user then true and let them edit
                return True
            else:
                return False


class UpdateOwnStatus(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.id == obj.user_profile.id
