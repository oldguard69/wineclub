from base.helpers import response_message
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404

from base.permissions import IsBusinessOwner, IsRetailer
from membership_program.models import MembershipProgram
from business.models import Business
from membership_program.retailer.serializers import MembershipProgramSerializer


class MembershipManagementView(GenericAPIView):
    permission_classes = [IsRetailer, IsBusinessOwner]

    @property
    def business(self):
        return get_object_or_404(Business, id=self.kwargs['business_id'])
    
    @property
    def membership_program(self):
        business = self.business
        return get_object_or_404(MembershipProgram, business__id=business.id)

    def get(self, request, *args, **kwargs):
        membership_program = self.membership_program
        serializer = MembershipProgramSerializer(membership_program)
        return Response(serializer.data, HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MembershipProgramSerializer(data=request.data)
        if MembershipProgram.objects.filter(business__id=kwargs['business_id']).exists():
            return Response(response_message('You can only have one Membership Program.'), HTTP_400_BAD_REQUEST)
        if serializer.is_valid(True):
            serializer.save(business=self.business)
            return Response(serializer.data, HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        membership_program = self.membership_program
        serializer = MembershipProgramSerializer(membership_program, request.data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        membership_program = self.membership_program
        membership_program.delete()
        return Response('', HTTP_204_NO_CONTENT)


class MembershipCustomerList(ListAPIView):
    pass