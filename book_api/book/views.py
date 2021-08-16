from rest_framework import generics
from rest_framework.response import Response


from book.models import Book
from book.serializer import BookSerializer
from genre.models import Genre
from publisher.models import Publisher

class BookList(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # def update(self, request, *args, **kwargs):
    #     serializer = BookSerializer(self.get_object(), data=request.data)
    #     data = request.data
    #     if serializer.is_valid():
    #         validated_data = serializer.data
    #         print(validated_data)
    #     else:
    #         print(serializer.data)
    #     return Response(data=serializer.data)