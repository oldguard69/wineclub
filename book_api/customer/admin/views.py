from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
import django_filters

from customer.models import Customer
from .serializers import CustomerSerializer
from employee.permission import HasAdminPermission
from user.models import User

class CustomerFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter('is_active', 'exact')
    fullname = django_filters.CharFilter('fullname', 'icontains')
    phone = django_filters.CharFilter('phone_number', 'icontains')


class CustomerListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (HasAdminPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomerFilter


def change_customer_active_state(pk, state):
    user = User.objects.get(id=pk)
    user.is_active = state
    user.save()

class ActivateCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, True)
            return Response({'msg': 'Customer has been activated'}, status.HTTP_200_OK)
        except User.DoesNotExist:
            return customer_does_not_exist_response()

class BlockCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, False)
            return Response({'msg': 'Customer has been blocked'}, status.HTTP_200_OK)
        except User.DoesNotExist:
            return customer_does_not_exist_response()


def customer_does_not_exist_response():
    return Response(
                {'msg': 'Customer with the given id does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )