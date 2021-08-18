from rest_framework import viewsets
import django_filters
from author.models import Author
from author.serializer import AuthorSerializer

class AuthorFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter('fullname', 'icontains')
    class Meta:
        model = Author
        fields = ['fullname']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = AuthorFilter