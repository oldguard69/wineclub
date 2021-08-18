from rest_framework import viewsets
import django_filters

from genre.models import Genre
from genre.serializers import GenreSerializer

class GenreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name', 'icontains')
    class Meta:
        model = Genre
        fields = ['name']

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = GenreFilter