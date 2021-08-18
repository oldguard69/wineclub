from rest_framework import viewsets
import django_filters

from publisher.serializer import PublisherSerializer
from publisher.models import Publisher

class PublisherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name', 'icontains')
    class Meta:
        model = Publisher
        fields = ['name']

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = PublisherFilter