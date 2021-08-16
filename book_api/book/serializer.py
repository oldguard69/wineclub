from rest_framework import serializers


from book.models import Book
from publisher.serializer import PublisherSerializer
from author.serializer import AuthorSerializer
from genre.serializers import GenreSerializer


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    author = AuthorSerializer(many=True, read_only=True)
    genre = GenreSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Book

    def update(self, instance, validated_data):
        print(validated_data)
        return instance