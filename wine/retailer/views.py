from rest_framework.generics import get_object_or_404
from base.permissions import IsBusinessOwner, IsRetailer
from business.models import Business
from rest_framework.viewsets import ModelViewSet

from wine.models import Wine
from .serializers import WineSerializer


class WineViewSet(ModelViewSet):
    permission_classes = [IsRetailer, IsBusinessOwner]
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

    @property
    def current_business(self):
        business_id = self.kwargs['business_id']
        business = get_object_or_404(Business, id=business_id)
        return business

    # filter to make sure winery can access their own resources
    def get_queryset(self):
        business = self.current_business
        return Wine.objects.filter(business=business)

    def perform_create(self, serializer):
        business = self.current_business
        serializer.save(business=business)