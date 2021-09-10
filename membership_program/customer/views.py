from base.permissions import IsCustomer
from rest_framework.generics import GenericAPIView, get_object_or_404
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from membership_program.models import MembershipProgram, Membership
from customer.models import Customer
from base.helpers import response_message

class RequestToJoinMembership(GenericAPIView):
    permission_classes = [IsCustomer]

    def get(self, request, business_id):
        membership_program = get_object_or_404(MembershipProgram, business_id)
        customer = get_object_or_404(Customer, user__id=request.user.id)
        membership = Membership.objects.create(
            membership_program=membership_program,
            customer=customer,
            date_request=timezone.now(),
            joined=False
        )
        membership.save()
        return Response(response_message('Your request has been sent.'), HTTP_200_OK)