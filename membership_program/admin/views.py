from rest_framework.viewsets import ReadOnlyModelViewSet


from base.permissions import HasAdminPermission
from membership_program.admin.serializers import MembershipProgramSerializer
from membership_program.models import MembershipProgram

class MembershipViewSet(ReadOnlyModelViewSet):
    permission_classes = [HasAdminPermission]
    queryset = MembershipProgram.objects.all()
    serializer_class = MembershipProgramSerializer
