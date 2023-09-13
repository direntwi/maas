from rest_framework import permissions


class UpdateDriverProfile(permissions.BasePermission):
    """Allows drivers to create their own profiles"""

    def has_object_permission(self, request, view, obj):
        # return super().has_object_permission(request, view, obj)
    
        """if the above code does not work for some reason, try the code below"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.id == request.user.id