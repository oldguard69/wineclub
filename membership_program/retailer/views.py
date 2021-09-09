from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.generics import GenericAPIView, get_object_or_404

from base.permissions import IsWinery
from membership_program.models import MembershipProgram
from business.models import Business
from membership_program.retailer.serializers import MembershipProgramSerializer

class MembershipView(GenericAPIView):
    permission_classes = [IsWinery]

    @property
    def business(self):
        return get_object_or_404(Business, user__id=self.request.user.id)
    
    @property
    def membership_program(self):
        business = self.business
        return get_object_or_404(MembershipProgram, business__id=business.id)

    def get(self, request):
        membership_program = self.membership_program
        serializer = MembershipProgramSerializer(membership_program)
        return Response(serializer.data)

    def post(self, request):
        serializer = MembershipProgramSerializer(data=request.data)
        if serializer.is_valid(True):
            serializer.save(business=self.business)
            return Response(serializer.data)

    def put(self, request):
        membership_program = self.membership_program
        serializer = MembershipProgramSerializer(membership_program, request.data)
        if serializer.is_valid(True):
            serializer.save()

    def delete(self, request):
        membership_program = self.membership_program
        membership_program.delete()
        return Response('', HTTP_204_NO_CONTENT)