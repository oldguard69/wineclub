from rest_framework.response import Response
from customer.models import Customer
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny


from wine.models import Wine
from wine.customer.serializers import WineSerializer
from base.permissions import IsCustomer
from base.helpers import response_message
import base.templates.notice_templates as notices

class WineViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = WineSerializer
    queryset = Wine.objects.all()


class FavoriteWineList(ListAPIView):
    permission_classes = [IsCustomer]
    serializer_class = WineSerializer
    
    def get_queryset(self):
        customer = get_object_or_404(Customer, user__id=self.request.user.id)
        return Wine.objects.filter(customer=customer)


class FavoriteWineAddRemove(CreateAPIView, DestroyAPIView):
    permission_classes = [IsCustomer]

    def post(self, request, *args, **kwargs):
        wine = get_object_or_404(Wine, id=kwargs['pk'])
        customer = Customer.objects.get(user__id=request.user.id)
        customer.favorite_wine.add(wine)
        customer.save()
        return Response(response_message(notices.WINE_ADDED_TO_FAVORITE))

    def delete(self, request, *args, **kwargs):
        wine = get_object_or_404(Wine, id=kwargs['pk'])
        customer = Customer.objects.get(user__id=request.user.id)
        customer.favorite_wine.remove(wine)
        customer.save()
        return Response(response_message(notices.WINE_REMOVED_FROM_FAVORITE))