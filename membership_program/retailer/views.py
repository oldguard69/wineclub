from django.utils import timezone
from base.helpers import get_validated_data, response_message
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.generics import GenericAPIView, ListAPIView, get_object_or_404
from django.db import transaction

from base.permissions import IsBusinessOwner, IsRetailer
from membership_program.models import Membership, MembershipProgram
from business.models import Business
from membership_program.retailer.serializers import MembershipCustomerListSerializer, MembershipProgramSerializer
from customer.models import Customer
import base.templates.notice_templates as notices
from membership_program.retailer.serializers import CustomerIdSerializer


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


class MembershipJoinedCustomers(ListAPIView):
    permission_classes = [IsBusinessOwner]
    serializer_class = MembershipCustomerListSerializer
    queryset = Customer.objects.filter(membership__joined=True)

    def get_queryset(self):
        membership_program = get_object_or_404(MembershipProgram, business__id=self.kwargs['business_id'])
        return Customer.objects.filter(
            membership__joined=True, 
            membership__membership_program__id=membership_program.id
        )


class MembershipRequestCustomers(ListAPIView):
    permission_classes = [IsBusinessOwner]
    serializer_class = MembershipCustomerListSerializer
    queryset = Customer.objects.filter(membership__joined=True)

    def get_queryset(self):
        membership_program = get_membership_program(self.kwargs['business_id'])
        return Customer.objects.filter(
            membership__joined=False, 
            membership__membership_program__id=membership_program.id
        )


# TODO: send email to customer
class AcceptMembershipRequest(GenericAPIView):
    @transaction.atomic
    def get(self, request, *args, **kwargs):
        validated_data, _ = get_validated_data(CustomerIdSerializer, request)
        membership = get_membership(kwargs['business_id'], validated_data.get('customer_id'))
        membership.date_join = timezone.now()
        membership.joined = True
        membership.save()
        return Response(response_message(notices.MEMBERSHIP_REQUEST_ACCEPTED), HTTP_200_OK)


# TODO: send email to customer
class DeclineMembershipRequest(GenericAPIView):
    @transaction.atomic
    def post(self, request, business_id):
        validated_data, _ = get_validated_data(CustomerIdSerializer, request)
        membership = get_membership(business_id, validated_data.get('customer_id'))
        membership.delete()
        return Response(response_message(notices.MEMBERSHIP_REQUEST_DECLINED), HTTP_200_OK)


# TODO: send email to customer
class RemoveMembership(GenericAPIView):
    @transaction.atomic
    def post(self, request, business_id):
        validated_data, _ = get_validated_data(CustomerIdSerializer, request)
        membership = get_membership(business_id, validated_data.get('customer_id'))
        membership.delete()
        return Response(response_message(notices.MEMBERSHIP_REMOVED), HTTP_200_OK)


def get_membership_program(business_id):
    return get_object_or_404(MembershipProgram, business__id=business_id)

def get_membership(business_id, customer_id):
    membership_program = get_membership_program(business_id)
    return get_object_or_404(
            Membership, 
            membership__membership_program__id=membership_program.id,
            customer__id=customer_id
        )