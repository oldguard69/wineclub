from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework import status

from customer.models import Customer
from base.helpers import get_validated_data, response_message
from .serializers import CustomerProfileSerializer, FavoriteRegionSerializer, FavoriteWineTypeSerializer
import base.templates.error_templates as errors
import base.templates.notice_templates as notices

# get customer profile
# update customer profile
class CustomerProfile(GenericAPIView):

    def get(self, request):
        customer = get_object_or_404(Customer, user__id=request.user.id)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        customer = get_object_or_404(Customer, user__id=request.user.id)
        validated_data, serializer = get_validated_data(CustomerProfileSerializer, request)
        result = serializer.update(customer, validated_data)
        if result == 'error':
            return Response(response_message(errors.SERVER_ERROR), status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(response_message(notices.PROFILE_UPDATED), status.HTTP_200_OK)


class UpdateFavoriteRegion(GenericAPIView):
    def post(self, request):
        customer = get_object_or_404(Customer, user__id=request.user.id)
        serializer = FavoriteRegionSerializer(customer, request.data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

class UpdateFavoriteWineType(GenericAPIView):
    def post(self, request):
        customer = get_object_or_404(Customer, user__id=request.user.id)
        serializer = FavoriteWineTypeSerializer(customer, request.data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)