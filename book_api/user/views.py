from django.db import transaction
from django.http.response import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from datetime import timedelta
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.mail import send_mail

from book_api import config
from user.serializers import (
    LoginSerializer, RegisterSerializer, 
    RequestUpdateEmailSerializer, VerifyUpdateEmailSerializer,
    UserProfileSerializer
    )
from book_api.helpers import get_validated_data, get_user_id
from user.models import User, UpdateEmailVerifyCode
from employee.models import Employee

# TODO: create stripe Customer and save it along with our Customer model
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


class Login(APIView):
    def post(self, request, format=None):
        validated_data, _ = get_validated_data(LoginSerializer, request)
        try:
            user = User.objects.get(email=validated_data.get('email'))
            if user.check_password(validated_data.get('password')):
                role = 'customer'
                if user.is_staff:
                    employee = Employee.objects.get(user__id=user.id)
                    role = employee.role
                refresh = RefreshToken.for_user(user)
                refresh['role'] = role
                return Response(
                    {'refresh': str(refresh), 'access': str(refresh.access_token)},
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {'msg': 'Password is incorrect.'}, 
                    status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {'msg': 'Account with the given email does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )


class RequestUpdateEmail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        validated_data, _ = get_validated_data(RequestUpdateEmailSerializer, request)
        new_email = validated_data.get('email')
        user = User.objects.get(id=request.auth.payload.get('user_id'))
        if new_email == user.email:
            return Response({'msg': f'{new_email} is your current email'})
        if is_email_has_been_used(new_email):
            return Response({'msg': 'Email is already used'})
        
        expiry_date = timezone.now() + timedelta(minutes=30)
        verify_code = uuid.uuid4()
        print(verify_code)
        code = UpdateEmailVerifyCode(
            current_email=user.email,
            new_email=new_email,
            verify_code=verify_code,
            expiry_date=expiry_date
        )
        send_mail(
            'Verify email',
            f'Your verify code is {verify_code}\n The verify code will be expired in 30 minutes',
            config.email,
            [new_email],
            fail_silently=False,
        )
        code.save()
        return Response({'request_id': code.id}, status.HTTP_200_OK)


class VerifyUpdateEmail(APIView):
    permission_classes = (IsAuthenticated, )

    @property
    def user_id(self):
        return get_user_id(self.request)
    # body: {verify_code, request_id} where id is UpdateEmailCode's id
    # Response: {msg}
    def post(self, request):
        validated_data, _ = get_validated_data(VerifyUpdateEmailSerializer, request)
        try:
            with transaction.atomic():
                code = UpdateEmailVerifyCode.objects.get(id=validated_data.get('request_id'))
                if timezone.now() > code.expiry_date:
                    code.delete()
                    return Response({'msg': 'The verify code has been expired.'})
                if is_email_has_been_used(code.new_email):
                    code.delete()
                    return Response({'msg': 'Email is already used.'})
                if validated_data.get('verify_code') != code.verify_code:
                    return Response({'msg': 'Your verify code is incorrect.'})
                user = User.objects.get(id=self.user_id)
                user.email = code.new_email
                user.save()
                code.delete()
                return Response({'msg': 'Your email has been updated.'})
        except IntegrityError:
            return Response(
                {'msg': 'Server error. Please try again later.'}, 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except UpdateEmailVerifyCode.DoesNotExist:
            return Response(
                {'msg': 'There are no current request to update email.'}, 
                status.HTTP_400_BAD_REQUEST
            )


def is_email_has_been_used(email):
    return User.objects.filter(email=email).exists()


class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request):
        pk = request.auth.payload.get('user_id')
        try:
            return User.objects.get(id=pk)
        except:
            raise Http404
    
    def get(self, request, format=None):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, format=None):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)


# class EmployeeChangePassword(APIView):
#     permission_classes = [IsEmployee]

#     def post(self, request, format=None):
#         serializer = ChangePasswordSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             validated_data = serializer.validated_data
#             empid = request.auth.payload.get('user_id')
#             try:
#                 emp = Employee.objects.get(id=empid)
#                 if not check_password(validated_data.get('password'), emp.password):
#                     return Response(
#                         {'msg': 'Your current password is incorrect.'},
#                         status.HTTP_400_BAD_REQUEST
#                     )
#                 else:
#                     if validated_data.get('new_password') != validated_data.get('confirm_new_password'):
#                         return Response(
#                             {'msg': 'Your new password and its confirm does not match.'},
#                             status.HTTP_400_BAD_REQUEST
#                         )
#                     else:
#                         hash_pw = make_password(validated_data.get('new_password'))
#                         emp.password = hash_pw
#                         emp.save()
#                         return Response({'msg': 'Your password has been changed'})
#             except Employee.DoesNotExist:
#                 return Response({'msg': 'Accout does not exist'}, status.HTTP_401_UNAUTHORIZED)