import os
import uuid
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.db.utils import IntegrityError
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView, get_object_or_404

from user.serializers import (
    ChangePasswordSerializer, LoginSerializer, RequestUpdateEmailSerializer, ResetPasswordSerializer, 
    VerifyUpdateEmailSerializer, ForgotPasswordSerializer
)
from base.helpers import get_validated_data, response_message, initialize_dotenv
from user.models import User, UpdateEmailVerifyCode, ResetPasswordCode
from employee.models import Employee
from base.constants import CUSTOMER_ROLE, RETAILER_ROLE, WINERY_ROLE
import base.templates.error_templates as errors
import base.templates.notice_templates as notices

initialize_dotenv()


class Login(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        validated_data, _ = get_validated_data(LoginSerializer, request)
        user = get_object_or_404(User, email=validated_data.get('email'))
        if user.check_password(validated_data.get('password')):
            role = CUSTOMER_ROLE
            if user.is_staff:
                employee = Employee.objects.get(user__id=user.id)
                role = employee.role
            elif user.is_retailer:
                role = RETAILER_ROLE
            refresh = RefreshToken.for_user(user)
            print(role)
            refresh['role'] = role
            return Response(
                {'refresh': str(refresh), 'access': str(refresh.access_token)},
                status.HTTP_200_OK
            )
        else:
            return Response(
                response_message(errors.INCORRECT_PASSWORD), 
                status.HTTP_400_BAD_REQUEST
            )


class RequestUpdateEmail(GenericAPIView):

    def post(self, request):
        validated_data, _ = get_validated_data(RequestUpdateEmailSerializer, request)
        new_email = validated_data.get('email')
        user = User.objects.get(id=request.user.id)
        if new_email == user.email:
            return Response(response_message( f'{new_email} is your current email'))
        if is_email_has_been_used(new_email):
            return Response(response_message(errors.EMAIL_IS_USED))
        
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
            os.getenv('email'),
            [new_email],
            fail_silently=False,
        )
        code.save()
        return Response({'request_id': code.id}, status.HTTP_200_OK)


class VerifyUpdateEmail(GenericAPIView):

    @property
    def user_id(self):
        return self.request.user.id

    def post(self, request):
        validated_data, _ = get_validated_data(VerifyUpdateEmailSerializer, request)
        code = get_object_or_404(UpdateEmailVerifyCode, id=validated_data.get('request_id'))
        try:
            with transaction.atomic():
                if timezone.now() > code.expiry_date:
                    code.delete()
                    return Response(response_message(errors.VERIFY_CODE_EXPIRED))
                if is_email_has_been_used(code.new_email):
                    code.delete()
                    return Response(response_message(errors.EMAIL_IS_USED))
                if validated_data.get('verify_code') != code.verify_code:
                    return Response(response_message(errors.VERIFY_CODE_INCORRECT))
                user = User.objects.get(id=self.user_id)
                user.email = code.new_email
                user.save()
                code.delete()
                return Response(response_message(notices.EMAIL_UPDATED))
        except IntegrityError:
            return Response(
                response_message(errors.SERVER_ERROR), 
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChangePassword(GenericAPIView):

    def post(self, request):
        validated_data, serializer = get_validated_data(ChangePasswordSerializer, request)
        user = get_object_or_404(User, pk=request.user.id)
        if not user.check_password(validated_data.get('password')):
            return Response(response_message(errors.CURRENT_PASSWORD_INCORRECT))
        if validated_data.get('new_password') != validated_data.get('confirm_new_password'):
            return Response(response_message(errors.CONFIRM_PASSWORD_NOT_MATCH))
        serializer.update(user, validated_data)
        return Response(response_message(notices.PASSWORD_UPDATED))


class ForgotPassword(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        validated_data, serializer = get_validated_data(ForgotPasswordSerializer, request)
        user = get_object_or_404(User, email=validated_data.get('email'))
        code = serializer.create(validated_data)
        send_mail(
            'Verify code for reset password',
            f'Your verify code is {code.verify_code}\n The verify code will be expired in 30 minutes',
            os.getenv('email'),
            [validated_data.get('email')],
            fail_silently=False,
        )
        return Response({'request_id': code.id}, status.HTTP_200_OK)


class ResetPassword(GenericAPIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        validated_data, serializer = get_validated_data(ResetPasswordSerializer, request)
        code = get_object_or_404(ResetPasswordCode, verify_code=validated_data.get('verify_code'))
        user = get_object_or_404(User, email=code.email)
        if timezone.now() > code.expiry_date:
            code.delete()
            return Response(response_message(errors.VERIFY_CODE_EXPIRED))
        serializer.update(user, validated_data)
        code.delete()
        return Response(response_message(notices.PASSWORD_UPDATED))
        

def is_email_has_been_used(email):
    return User.objects.filter(email=email).exists()