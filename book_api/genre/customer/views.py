from rest_framework.viewsets import ReadOnlyModelViewSet
import django_filters

from genre.models import Genre
from .serializers import GenreSerializer

class GenreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name', 'icontains')
    

class GenreViewSet(ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = GenreFilter