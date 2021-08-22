import django_filters
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from book.models import Book
from .serializers import BookSerializer, BookUpdateSerializer



class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter('title', 'icontains')
    genre = django_filters.CharFilter('genre__name', 'icontains')
    publisher = django_filters.CharFilter('publisher__name', 'icontains')
    author = django_filters.CharFilter('author__fullname', 'icontains')

    class Meta:
        model = Book
        fields = ['isbn'] # genrerate exact lookup for isbn

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_serializer_class(self):
        request = self.request
        if request.method == 'PUT' or request.method == 'POST':
            return BookUpdateSerializer
        else:
            return BookSerializer