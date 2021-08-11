from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    '''Only allow owners of an object to edit it'''
    def has_object_permission(self, request, view, obj):
        # read permission are allowd to any request
        # allow GET, HEAD, OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissio are only allowd to the owner of the snippet
        return obj.owner == request.user
