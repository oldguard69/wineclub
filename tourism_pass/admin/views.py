from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


from tourism_pass.models import TourismPass
from base.permissions import HasAdminPermission
from tourism_pass.admin.serializers import TourismPassSerializer

class TourismPassViewSet(ReadOnlyModelViewSet):
    permission_classes = [HasAdminPermission]
    queryset = TourismPass.objects.all()
    serializer_class = TourismPassSerializer


class TourismPassOfAWinery(ListAPIView):
    permission_classes = [HasAdminPermission]
    serializer_class = TourismPassSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return TourismPass.objects.filter(winery__id=pk)