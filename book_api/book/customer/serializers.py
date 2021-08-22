from rest_framework import serializers

from book.models import Book, BookImage
from publisher.customer.serializers import PublisherSerializer
from author.customer.serializers import AuthorSerializer
from genre.customer.serializers import GenreSerializer



class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(read_only=True)
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Book


    def get_image_url(self, obj):
        return [i["image_url"] for i in BookImage.objects.values('image_url').filter(book__id=obj.id)]