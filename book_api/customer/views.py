from django.http.response import Http404
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from customer.models import Customer
from customer.serializers import CustomerSerializer
from customer.filters import CustomerFilter
from employee.permission import HasAdminPermission


# List and detail customer
# For ADMIN ONLY
class CustomerListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (HasAdminPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomerFilter


def change_customer_active_state(pk, state):
    customer = Customer.objects.get(id=pk)
    customer.is_active = state
    customer.save()

class ActivateCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, True)
            return Response({'msg': 'Customer has been activated'}, status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(
                {'msg': 'Customer with the given id does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )

class BlockCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, False)
            return Response({'msg': 'Customer has been blocked'}, status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(
                {'msg': 'Customer with the given id does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )
