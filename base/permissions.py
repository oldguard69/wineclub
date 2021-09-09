from rest_framework import permissions
from base.constants import CUSTOMER_ROLE, EMP_ROLE, ADMIN_ROLE, WINERY_ROLE

def get_role(request):
    return request.auth.payload.get('role')

class HasAdminPermission(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and get_role(request) == ADMIN_ROLE
    
    
# use request.auth.payload instead of auxilary variable because we need to ensure isAuthenticated come first    
class IsEmployee(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and (
            get_role(request) == ADMIN_ROLE
            or get_role(request) == EMP_ROLE
        )


class IsWinery(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and get_role(request) == WINERY_ROLE

class IsCustomer(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and get_role(request) == CUSTOMER_ROLE

# class IsBusinessOwner(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         return super().has_permission(request, view) and get_role == 