from rest_framework import permissions
from base.constants import CUSTOMER_ROLE, EMP_ROLE, ADMIN_ROLE, WINERY_ROLE, RETAILER_ROLE
from business.models import Business

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



class IsRetailer(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and get_role(request) == RETAILER_ROLE

class IsCustomer(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and get_role(request) == CUSTOMER_ROLE

# # TODO: check if user carry in JWT own  business id
# class IsBusinessOwner(permissions.IsAuthenticated):
#     def has_permission(self, request, view):
#         businesses = Business.objects.filter(user__id=request.user.id).values('id')
#         business_ids = set([i['id'] for i in businesses])
#         business_url_param = view.kwargs['business_id']
#         return super().has_permission(request, view) and business_url_param in business_ids


class IsBusinessOwner(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        businesses = Business.objects.filter(user__id=request.user.id).values('id')
        business_ids = set([i['id'] for i in businesses])
        business_url_param = view.kwargs['business_id']
        return (
            super().has_permission(request, view) 
            and get_role(request) == RETAILER_ROLE
            and business_url_param in business_ids
        )
