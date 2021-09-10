from rest_framework.viewsets import ModelViewSet
import uuid

from reward_program.retailer.serializers import RewardProgramSerialzier
from business.models import Business
from base.permissions import IsRetailer
from reward_program.models import RewardProgram

class RewardProgramViewSet(ModelViewSet):
    permission_classes = [IsRetailer]
    queryset = RewardProgram.objects.all()
    serializer_class = RewardProgramSerialzier

    def get_queryset(self):
        business = Business.objects.get(user__id=self.request.user.id)
        return RewardProgram.objects.filter(business=business)

    def perform_create(self, serializer):
        business = Business.objects.get(user__id=self.request.user.id)
        serializer.save(business=business, reward_code=uuid.uuid4())