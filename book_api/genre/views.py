from rest_framework import generics, viewsets

from genre.models import Genre
from genre.serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer