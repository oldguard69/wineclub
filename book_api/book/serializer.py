from rest_framework import serializers

from book.models import Book
from publisher.serializer import PublisherSerializer
from author.serializer import AuthorSerializer
from genre.serializers import GenreSerializer

class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Book

# genre, publisher, author property is object
class BookSerializer(BookUpdateSerializer):
    publisher = PublisherSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)