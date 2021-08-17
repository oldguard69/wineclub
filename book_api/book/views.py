from rest_framework import generics, serializers
from rest_framework.response import Response


from book.models import Book
from book.serializer import BookSerializer, BookUpdateSerializer
from genre.models import Genre
from publisher.models import Publisher

class BookList(generics.ListCreateAPIView):
    
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()
        if self.request.method == 'GET':
            query_params = self.request.query_params
            genre_name = query_params.get('genre')
            publisher_name = query_params.get('publisher')
            author_fullname = query_params.get('author')
            book_name = query_params.get('book')
            isbn = query_params.get('isbn')
            if genre_name is not None:
                queryset = Book.objects.filter(genre__name__icontains=genre_name)
            elif publisher_name is not None:
                queryset = Book.objects.filter(publisher__name__icontains=publisher_name)
            elif author_fullname is not None:
                queryset = Book.objects.filter(author__fullname__icontains=author_fullname)
            elif book_name is not None:
                queryset = Book.objects.filter(title__icontainers=book_name)
            elif isbn is not None:
                queryset = Book.objects.filter(isbn=isbn)
        return queryset

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        request = self.request
        if request.method == 'PUT':
            return BookUpdateSerializer
        else:
            return BookSerializer