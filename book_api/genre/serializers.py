from django.db.models import fields
from rest_framework import serializers
from genre.models import Genre

class GenreSerializer(serializers.ModelSerializer):
    name_length = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'

    def get_name_length(self, obj):
        return len(obj.name)