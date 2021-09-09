from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView

from employee.employee.serializers import EmployeeProfileSerializer, EmployeeProfileUpdateSerializer
from employee.models import Employee
from base.helpers import get_user_id, response_message
from user.models import User
import base.templates.notice_templates as notices

# Get employee profile
# Update employee profile
class EmployeeProfile(GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeProfileSerializer

    def get(self, request):
        employee = Employee.objects.get(user__id=get_user_id(request))
        serializer = EmployeeProfileSerializer(employee)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        user = User.objects.get(id=get_user_id(request))
        serializer = EmployeeProfileUpdateSerializer(user, request.data, )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(response_message(notices.PROFILE_UPDATED), status.HTTP_200_OK)

