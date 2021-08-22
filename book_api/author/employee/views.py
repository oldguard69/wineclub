from rest_framework.viewsets import ModelViewSet
import django_filters

# class CreateUpdateDestroyViewSet(
#     mixins.CreateModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ):
#     pass


from employee.permission import IsEmployee
from .serializers import AuthorSerializer
from author.models import Author


class AuthorFilter(django_filters.FilterSet):
    fullname = django_filters.CharFilter('fullname', 'icontains')
    

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsEmployee]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_class = AuthorFilter