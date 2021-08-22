from rest_framework import viewsets
import django_filters
from author.models import Author
from .serializers import AuthorSerializer


class AuthorFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter('fullname', 'icontains')
    

class AuthorListRetrieveVS(viewsets.ReadOnlyModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = AuthorFilter