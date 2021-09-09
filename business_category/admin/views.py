from base.permissions import HasAdminPermission
from rest_framework.viewsets import ModelViewSet


from business_category.admin.serializers import BusinessCategorySerializer
from business_category.models import BusinessCategory

class BusinessCategoryViewSet(ModelViewSet):
    serializer_class = BusinessCategorySerializer
    permission_classes = [HasAdminPermission]
    queryset = BusinessCategory.objects.all()