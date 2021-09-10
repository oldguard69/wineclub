from rest_framework.generics import get_object_or_404
from base.permissions import IsBusinessOwner, IsRetailer
from business.models import Business
from tourism_pass.retailer.serializers import TourismPassSerializer
from rest_framework.viewsets import ModelViewSet
import uuid

from tourism_pass.models import TourismPass

class TourismViewSet(ModelViewSet):
    permission_classes = [IsRetailer, IsBusinessOwner]
    serializer_class = TourismPassSerializer
    queryset = TourismPass.objects.all()

    @property
    def current_business(self):
        business_id = self.kwargs['business_id']
        return get_object_or_404(Business, id=business_id)

    def get_queryset(self):
        business = self.current_business
        return TourismPass.objects.filter(business=business)

    
    def perform_create(self, serializer):
        business = self.current_business
        serializer.save(business=business, qr_code=uuid.uuid4())