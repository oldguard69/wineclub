from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404


from base.helpers import response_message
from base.permissions import HasAdminPermission
from subscription.models import Subscription
from subscription.admin.serializers import (
    SubscriptionSerializer, SubscriptionCreateSerializer, 
    SubscriptionUpdateSerializer
)
import base.templates.notice_templates as notices

class SubscriptionListCreate(GenericAPIView):
    permission_classes = [HasAdminPermission]

    def get(self, request):
        sub = Subscription.objects.all()
        serializer = SubscriptionSerializer(sub, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionCreateSerializer(data=request.data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(response_message(notices.SUBSCRIPTION_CREATED), status.HTTP_200_OK)


class SubscriptionRetrieveUpdate(GenericAPIView):
    permission_classes = [HasAdminPermission]

    def get(self, request, pk):
        sub = get_object_or_404(Subscription, pk=pk)
        serializer = SubscriptionSerializer(sub)
        return Response(serializer.data)

    def put(self, request, pk):
        sub = get_object_or_404(Subscription, pk=pk)
        serializer = SubscriptionUpdateSerializer(sub, request.data)
        if serializer.is_valid(True):
            serializer.save()
            return Response(response_message(notices.SUBSCRIPTION_UPDATED), status.HTTP_200_OK)
