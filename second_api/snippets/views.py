from rest_framework import generics, permissions, renderers, viewsets # serializers, status, mixins
from django.contrib.auth.models import User
# from django.http import HttpResponse
# from django.http.response import Http404
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, renderer_classes
from rest_framework.reverse import reverse

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })

# ============================================ generic class-based view ==============================================
class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # @action decorator to create a custom action, named highlight. 
    # This decorator can be used to add any custom endpoints 
    # that don't fit into the standard create/update/delete style.
    # Default response to GET, can customize thought 'method' argument
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

# class SnippetList(generics.ListCreateAPIView):
#     '''List or create a new snippet'''
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)

# class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]

#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)


# UserViewSet automatically provides 'list' and 'retrieve' actions
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer




# ============================================ class-based view using mixin ==============================================
# The base class provides the core functionality, and mixin classess provide .list() and .create()
# class SnippetList(
#                     mixins.ListModelMixin, 
#                     mixins.CreateModelMixin,
#                     generics.GenericAPIView
#                 ):
#     '''List or create a new snippet'''
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class SnippetDetail(
#                     mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView
#                 ):

#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)





# # ============================================ class-based view ==================================================
# class SnippetList(APIView):
#     '''List or create a new snippet'''

#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         serializers = SnippetSerializer(snippets, many=True)
#         return Response(serializers.data)
    
#     def post(self, request, format=None):
#         serializers = SnippetSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# class SnippetDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Snippet.objects.get(pk=pk)
#         except Snippet.DoesNotExist:
#             raise Http404
    
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializers = SnippetSerializer(snippet)
#         return Response(serializers.data)
    
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializers = SnippetSerializer(snippet, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# ================================= Function-based view ===========================================================
# @api_view(['GET', 'POST'])
# def snippet_list(request, format=None):
#     '''List or create a new snippet'''
#     if request.method == 'GET':
#         snippets = Snippet.objects.all()
#         serializers = SnippetSerializer(snippets, many=True)
#         return Response(serializers.data)
    
#     elif request.method == 'POST':
#         serializers = SnippetSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk, format=None):
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializers = SnippetSerializer(snippet)
#         return Response(serializers.data)
    
#     elif request.method == 'PUT':
#         serializers = SnippetSerializer(snippet, data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)