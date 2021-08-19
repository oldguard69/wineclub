from rest_framework import serializers
from rest_framework.decorators import permission_classes

from book.models import Book, BookImage
from publisher.serializers import PublisherSerializer
from author.serializers import AuthorSerializer
from genre.serializers import GenreSerializer


# genre, publisher, author property are their id
class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Book

# genre, publisher, author property are object
class BookSerializer(BookUpdateSerializer):
    publisher = PublisherSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()


    def get_image_url(self, obj):
        return [i["image_url"] for i in BookImage.objects.values('image_url').filter(book__id=obj.id)]