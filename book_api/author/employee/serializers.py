from rest_framework import serializers

from author.models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Author