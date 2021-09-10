from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

from business.models import Business
from base.helpers import get_validated_data, response_message
from business.retailer.serializers import BusinessSerializer, BusinessCreateSerializer
import base.templates.error_templates as errors
import base.templates.notice_templates as notices


class BusinessViewSet(ModelViewSet):
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()

    def get_queryset(self):
        return Business.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        validated_data, serializer = get_validated_data(
            BusinessCreateSerializer, request
        )
        result = serializer.save(user=request.user)
        if result == 'error':
            return Response(
                response_message(errors.SERVER_ERROR),
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(response_message(notices.ACCOUNT_CREATED), status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        business = get_object_or_404(Business, id=kwargs['pk'])
        serializer = BusinessSerializer(business, request.data)
        if serializer.is_valid(True):
            validated_data = serializer.validated_data
            if is_email_invalid_for_update(business, validated_data):
                return Response(response_message(errors.EMAIL_IS_USED), status.HTTP_400_BAD_REQUEST)
            else:
                result = serializer.save()
                if result == 'error':
                    return Response(response_message(errors.SERVER_ERROR), status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(response_message(notices.PROFILE_UPDATED), status.HTTP_200_OK)


def is_email_invalid_for_update(business, validated_data):
    email = validated_data.get('email')
    return business.email != email and Business.objects.filter(email=email).exists()