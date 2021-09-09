from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from django_filters import rest_framework as filters
import django_filters

from business.models import Business
from business.admin.serializers import BusinessSerializer
from base.permissions import HasAdminPermission
from user.models import User
from base.helpers import response_message
import base.templates.notice_templates as notices

class BusinessFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter('user__is_active', 'exact')
    first_name = django_filters.CharFilter('user__first_name', 'icontains')
    last_name = django_filters.CharFilter('user__last_name', 'icontains')
    phone = django_filters.CharFilter('user__phone', 'icontains')

# List all business
# Retrieve a single business
class BusinessListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = (HasAdminPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BusinessFilter


def change_business_active_state(pk, state):
    business = get_object_or_404(Business, pk=pk)
    business.user.is_active = state
    business.user.save()

class ActivateBusiness(GenericAPIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_business_active_state(pk, True)
            return Response(response_message(notices.WINERY_ACTIVATED), status.HTTP_200_OK)
        except User.DoesNotExist:
            return winery_does_not_exist_response()


class BlockBusiness(GenericAPIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_business_active_state(pk, False)            
            return Response(response_message(notices.WINERY_BLOCKED), status.HTTP_200_OK)
        except User.DoesNotExist:
            return winery_does_not_exist_response()


def winery_does_not_exist_response():
    return Response(
                response_message(notices.WINERY_NOT_EXIST), 
                status.HTTP_404_NOT_FOUND
            )