from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters import rest_framework as filters
import django_filters

from .serializers import BookSerializer
from book.models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter('title', 'icontains')
    genre = django_filters.CharFilter('genre__name', 'icontains')
    publisher = django_filters.CharFilter('publisher__name', 'icontains')
    author = django_filters.CharFilter('author__fullname', 'icontains')

    class Meta:
        model = Book
        fields = ['isbn'] # genrerate exact lookup for isbn

class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter