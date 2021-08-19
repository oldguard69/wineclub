from rest_framework import permissions

class HasAdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.auth.payload.get('role') == 'admin'
    
    
# use request.auth.payload instead of auxilary variable because we need to ensure isAuthenticated come first    
class IsEmployee(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            request.auth.payload.get('role') == 'admin' 
            or request.auth.payload.get('role') == 'emp')