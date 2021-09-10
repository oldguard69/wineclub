from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
import uuid

from reward_program.retailer.serializers import RewardProgramSerialzier
from business.models import Business
from base.permissions import IsBusinessOwner, IsRetailer
from reward_program.models import RewardProgram

class RewardProgramViewSet(ModelViewSet):
    permission_classes = [IsRetailer, IsBusinessOwner]
    queryset = RewardProgram.objects.all()
    serializer_class = RewardProgramSerialzier

    @property
    def current_business(self):
        business_id = self.kwargs['business_id']
        business = get_object_or_404(Business, id=business_id)
        return business

    def get_queryset(self):
        business = self.current_business
        return RewardProgram.objects.filter(business=business)

    def perform_create(self, serializer):
        business = self.current_business
        serializer.save(business=business, reward_code=uuid.uuid4())