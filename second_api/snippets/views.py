# ================= views as regular Django views =========================
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# csrf_exempt allow POST, PUT from client don't have CSRF token
@csrf_exempt
def snippet_list(request):
    '''List or create a new snippet'''
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializers = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializers.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = SnippetSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data, status=201)
        return JsonResponse(serializers.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == "GET":
        serializers = SnippetSerializer(snippet)
        return JsonResponse(serializers.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializers = SnippetSerializer(snippet, data=data)
        if serializers.is_valid():
            serializers.save()
            return JsonResponse(serializers.data)
        return JsonResponse(serializers.errors, status=400)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)