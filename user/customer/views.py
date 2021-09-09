from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import RegisterSerializer
from base.helpers import get_validated_data, response_message
from user.models import User
import base.templates.notice_templates as notices
import base.templates.error_templates as errors

class Register(APIView):
    def post(self, request, format=None):
        validated_data, serializer = get_validated_data(RegisterSerializer, request)
        if User.objects.filter(email=validated_data.get('email')).exists():
            return Response(response_message(errors.EMAIL_IS_USED), status.HTTP_200_OK)
        else:
            result = serializer.create(validated_data)
            if result == 'error':
                return Response(
                    response_message(errors.SERVER_ERROR),
                    status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response(response_message(notices.ACCOUNT_CREATED), status.HTTP_200_OK)