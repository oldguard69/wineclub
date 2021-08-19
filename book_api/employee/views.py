from django.contrib.auth.hashers import check_password, make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status, viewsets
from django.db import transaction

from customer.serializers import LoginSerializer, ChangePasswordSerializer
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.permission import AdminPermission


class EmployeeLogin(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            try:
                emp = Employee.objects.get(email=validated_data.get('email'))
                if check_password(validated_data.get('password'), emp.password):
                    refresh = RefreshToken.for_user(emp)
                    refresh['role'] = emp.role
                    return Response(
                        {'refresh': str(refresh), 'access': str(refresh.access_token)},
                        status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'msg': 'Password is incorrect.'}, 
                        status.HTTP_400_BAD_REQUEST
                    )
            except Employee.DoesNotExist:
                return Response(
                    {'msg': 'Account with the given email does not exist'}, 
                    status.HTTP_401_UNAUTHORIZED
                )


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, AdminPermission]

    def list(self, request, *args, **kwargs):
        if hasattr(request.auth, 'payload'):
            print(request.auth.payload)
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        raw_password = request.data.get('password')
        hash_pw = make_password(raw_password)
        request.data["password"] = hash_pw
        return super().create(request, *args, **kwargs)


class EmployeeChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
            empid = request.auth.payload.get('user_id')
            try:
                emp = Employee.objects.get(id=empid)
                if not check_password(validated_data.get('password'), emp.password):
                    return Response(
                        {'msg': 'Your current password is incorrect.'},
                        status.HTTP_400_BAD_REQUEST
                    )
                else:
                    if validated_data.get('new_password') != validated_data.get('confirm_new_password'):
                        return Response(
                            {'msg': 'Your new password and its confirm does not match.'},
                            status.HTTP_400_BAD_REQUEST
                        )
                    else:
                        hash_pw = make_password(validated_data.get('new_password'))
                        emp.password = hash_pw
                        emp.save()
                        return Response({'msg': 'Your password has been changed'})
            except Employee.DoesNotExist:
                return Response({'msg': 'Accout does not exist'}, status.HTTP_401_UNAUTHORIZED)
