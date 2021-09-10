from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


from wine.models import Wine
from base.permissions import HasAdminPermission
from wine.admin.serializers import WineSerializer

class WineViewSet(ReadOnlyModelViewSet):
    permission_classes = [HasAdminPermission]
    queryset = Wine.objects.all()
    serializer_class = WineSerializer


class WineOfABusiness(ListAPIView):
    permission_classes = [HasAdminPermission]
    serializer_class = WineSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Wine.objects.filter(business__id=pk)
    