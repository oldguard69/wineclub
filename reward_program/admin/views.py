from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet


from reward_program.admin.serializers import RewardProgramSerializer
from reward_program.models import RewardProgram
from base.permissions import HasAdminPermission

class RewardProgramViewSet(ReadOnlyModelViewSet):
    permission_classes = [HasAdminPermission]
    queryset = RewardProgram.objects.all()
    serializer_class = RewardProgramSerializer


class RewardProgramOfABusiness(ListAPIView):
    permission_classes = [HasAdminPermission]
    serializer_class = RewardProgramSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return RewardProgram.objects.filter(business__id=pk)