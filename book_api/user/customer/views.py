from django.db import transaction
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from book_api import config
from .serializers import RegisterSerializer
from book_api.helpers import get_validated_data
from user.models import User



class Register(APIView):
    def post(self, request, format=None):
        data, serializer = get_validated_data(RegisterSerializer, request)
        if User.objects.filter(email=data.get('email')).exists():
            return Response({'msg': 'Email has been used'}, status.HTTP_200_OK)
        else:
            result = serializer.create(data)
            if result == 'error':
                return Response(
                    data={'msg': 'Server error. Please try again later'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({'msg': 'Account created successfully'}, status.HTTP_200_OK)