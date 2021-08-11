# ================= views as regular Django views =========================
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

#s using format suffixes gives us URLs that explicitly refer to a given format
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    '''List or create a new snippet'''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return Response(serializers.data)
    
    elif request.method == 'POST':
        serializers = SnippetSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializers = SnippetSerializer(snippet)
        return Response(serializers.data)
    
    elif request.method == 'PUT':
        serializers = SnippetSerializer(snippet, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)