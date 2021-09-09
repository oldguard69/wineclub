from base.permissions import IsWinery
from business.models import Business
from rest_framework.viewsets import ModelViewSet

from wine.models import Wine
from .serializers import WineSerializer


class WineViewSet(ModelViewSet):
    permission_classes = [IsWinery]
    queryset = Wine.objects.all()
    serializer_class = WineSerializer

    # filter to make sure winery can access their own resources
    def get_queryset(self):
        business = Business.objects.get(user__id=self.request.user.id)
        return Wine.objects.filter(business=business)

    def perform_create(self, serializer):
        business = Business.objects.get(user__id=self.request.user.id)
        serializer.save(business=business)