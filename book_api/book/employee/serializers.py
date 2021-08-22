from rest_framework import serializers

from book.models import Book, BookImage
from publisher.employee.serializers import PublisherSerializer
from author.employee.serializers import AuthorSerializer
from genre.employee.serializers import GenreSerializer
from employee.permission import IsEmployee

# genre, publisher, author property are their id
class BookUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Book

# genre, publisher, author property are object
class BookSerializer(BookUpdateSerializer):
    permission_classes = [IsEmployee]
    publisher = PublisherSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()


    def get_image_url(self, obj):
        return [i["image_url"] for i in BookImage.objects.values('image_url').filter(book__id=obj.id)]