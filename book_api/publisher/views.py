from rest_framework import generics, viewsets

from publisher.serializer import PublisherSerializer
from publisher.models import Publisher

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer