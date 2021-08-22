from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db import transaction

from book_api.helpers import get_validated_data
from employee.models import Employee
from .serializers import EmployeeSerializer
from employee.permission import HasAdminPermission
from user.models import User


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [HasAdminPermission]


    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data, serializer = get_validated_data(EmployeeSerializer, request)
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



