from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response

from business.models import Business
from base.permissions import IsCustomer
from business.customer.serializers import BusinessSerializer
from customer.models import Customer
from base.helpers import response_message
import base.templates.notice_templates as notices

class BusinessViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsCustomer]
    serializer_class = BusinessSerializer
    queryset = Business.objects.all()


class FavoriteBusinessList(ListAPIView):
    permission_classes = [IsCustomer]
    serializer_class = BusinessSerializer
    
    def get_queryset(self):
        customer = get_object_or_404(Customer, user__id=self.request.user.id)
        return Business.objects.filter(customer=customer)


class FavoriteBusinessAddRemove(CreateAPIView, DestroyAPIView):
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        business = get_object_or_404(Business, id=kwargs['pk'])
        customer = Customer.objects.get(user__id=request.user.id)
        customer.favorite_business.add(business)
        customer.save()
        return Response(response_message(notices.BUSINESS_ADDED_TO_FAVORITE))

    def delete(self, request, *args, **kwargs):
        business = get_object_or_404(Business, id=kwargs['pk'])
        customer = Customer.objects.get(user__id=request.user.id)
        customer.favorite_business.remove(business)
        return Response(response_message(notices.BUSINESS_REMOVED_FROM_FAVORITE))