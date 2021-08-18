import django_filters
from book.models import Book

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter('title', 'icontains')
    genre = django_filters.CharFilter('genre__name', 'icontains')
    publisher = django_filters.CharFilter('publisher__name', 'icontains')
    author = django_filters.CharFilter('author__fullname', 'icontains')
    # isbn = django_filters.CharFilter('isbn', 'contains')

    class Meta:
        model = Book
        fields = ['isbn'] # genrerate exact lookup for isbn