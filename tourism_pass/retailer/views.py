from base.permissions import IsRetailer
from business.models import Business
from tourism_pass.retailer.serializers import TourismPassSerializer
from rest_framework.viewsets import ModelViewSet
import uuid

from tourism_pass.models import TourismPass

class TourismViewSet(ModelViewSet):
    permission_classes = [IsRetailer]
    serializer_class = TourismPassSerializer
    queryset = TourismPass.objects.all()

    def get_queryset(self):
        business = Business.objects.get(user__id=self.request.user.id)
        return TourismPass.objects.filter(business=business)

    
    def perform_create(self, serializer):
        business = Business.objects.get(user__id=self.request.user.id)
        serializer.save(business=business, qr_code=uuid.uuid4())