from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework as filters
import django_filters


from customer.models import Customer
from .serializers import CustomerSerializer
from base.permissions import HasAdminPermission
from user.models import User
from base.helpers import response_message
import base.templates.notice_templates as notices

class CustomerFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter('user__is_active', 'exact')
    first_name = django_filters.CharFilter('user__first_name', 'icontains')
    last_name = django_filters.CharFilter('user__last_name', 'icontains')
    phone = django_filters.CharFilter('user__phone', 'icontains')

# List all customer
# Retrieve a single customer
class CustomerListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (HasAdminPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomerFilter


class ActivateCustomer(GenericAPIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            print('herer')
            change_customer_active_state(pk, True)
            return Response(response_message(notices.CUSTOMER_ACTIVATED), status.HTTP_200_OK)
        except User.DoesNotExist:
            return customer_does_not_exist_response()


class BlockCustomer(GenericAPIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, False)            
            return Response(response_message(''), status.HTTP_200_OK)
        except User.DoesNotExist:
            return customer_does_not_exist_response()


def customer_does_not_exist_response():
    return Response(
                response_message(notices.CUSTOMER_NOT_EXIST), 
                status.HTTP_404_NOT_FOUND
            )

def change_customer_active_state(pk, state):
    customer = Customer.objects.get(id=pk)
    customer.user.is_active = state
    customer.user.save()