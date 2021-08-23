from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from order.models import Order
from .serializers import OrderSerializer
from order.models import Order
from employee.permission import IsEmployee


class OrderVS(ModelViewSet):
    serializers = OrderSerializer
    queryset = Order.objects.all()
    permissions = [IsEmployee]


class AcceptOrder(APIView):
    permission_classes = [IsEmployee]
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'success'
        order.save()
        return Response({'msg': 'Order created successfully'}, status.HTTP_200_OK)


class CancelOrder(APIView):
    permission_classes = [IsEmployee]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = 'cancel'
        order.save()
        return Response({'msg': 'Order has been canceled'}, status.HTTP_200_OK)
