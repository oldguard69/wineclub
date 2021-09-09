from rest_framework.viewsets import ReadOnlyModelViewSet


from business_category.retailer.serializers import BusinessCategorySerializer
from business_category.models import BusinessCategory

class BusinessCategoryViewSet(ReadOnlyModelViewSet):
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer