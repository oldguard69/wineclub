from rest_framework import generics, serializers
from rest_framework.response import Response
from django_filters import rest_framework as filters

from book.models import Book
from book.serializer import BookSerializer, BookUpdateSerializer
from genre.models import Genre
from publisher.models import Publisher
from book.filter import BookFilter

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BookFilter


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        request = self.request
        if request.method == 'PUT':
            return BookUpdateSerializer
        else:
            return BookSerializer