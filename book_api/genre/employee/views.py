from rest_framework import viewsets
import django_filters

from genre.models import Genre
from .serializers import GenreSerializer
from employee.permission import IsEmployee


class GenreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name', 'icontains')
    

class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = (IsEmployee,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = GenreFilter