from django.http.response import Http404
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters import rest_framework as filters
import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.utils import timezone
from book_api import config
from customer.models import Customer, UpdateEmailVerifyCode
from customer.serializers import (CustomerSerializer, LoginSerializer, 
                                  CustomerProfileSerializer, RegisterSerializer,
                                  RequestUpdateEmailSerializer, VerifyUpdateEmailSerializer)
from customer.filters import CustomerFilter
from employee.permission import HasAdminPermission


# List and detail customer
# For ADMIN ONLY
class CustomerListRetrieveViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (HasAdminPermission, )
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CustomerFilter


def change_customer_active_state(pk, state):
    customer = Customer.objects.get(id=pk)
    customer.is_active = state
    customer.save()

class ActivateCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, True)
            return Response({'msg': 'Customer has been activated'}, status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(
                {'msg': 'Customer with the given id does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )

class BlockCustomer(APIView):
    permission_classes = (HasAdminPermission, )

    @transaction.atomic
    def get(self, request, pk, format=None):
        try:
            change_customer_active_state(pk, False)
            return Response({'msg': 'Customer has been blocked'}, status.HTTP_200_OK)
        except Customer.DoesNotExist:
            return Response(
                {'msg': 'Customer with the given id does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )



# TODO: create stripe Customer and save it along with our Customer model
class Register(APIView):
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if Customer.objects.filter(email=data.get('email')).exists():
            return Response({'msg': 'Email has been used'}, status.HTTP_200_OK)
        else:
            hash_pw = make_password(data.get('password'))
            data["password"] = hash_pw
            result = serializer.create(data)
            if result == 'error':
                return Response(
                    data={'msg': 'Server error. Please try again later'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({'msg': 'Account created successfully'}, status.HTTP_200_OK)


class Login(APIView):
    def post(self, request, format=None):
        validated_data = get_validated_data(LoginSerializer, request)
        try:
            customer = Customer.objects.get(email=validated_data.get('email'))
            if check_password(validated_data.get('password'), customer.password):
                refresh = RefreshToken.for_user(customer)
                refresh['role'] = 'customer'
                return Response(
                    {'refresh': str(refresh), 'access': str(refresh.access_token)},
                    status.HTTP_200_OK
                )
            else:
                return Response(
                    {'msg': 'Password is incorrect.'}, 
                    status.HTTP_400_BAD_REQUEST
                )
        except Customer.DoesNotExist:
            return Response(
                {'msg': 'Account with the given email does not exist'}, 
                status.HTTP_404_NOT_FOUND
            )

                
class CustomerProfile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request):
        pk = request.auth.payload.get('user_id')
        try:
            return Customer.objects.get(id=pk)
        except:
            raise Http404
    
    def get(self, request, format=None):
        customer = self.get_object(request)
        serializer = CustomerProfileSerializer(customer)
        return Response(serializer.data, status.HTTP_200_OK)
    
    def put(self, request, format=None):
        customer = self.get_object(request)
        print(customer)
        serializer = CustomerProfileSerializer(customer, request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)


class RequestChangeEmail(APIView):
    permission_classes = (IsAuthenticated,)

    # body: {email}
    # response: UpdateEmailCode.id
    def post(self, request):
        validated_data = get_validated_data(RequestUpdateEmailSerializer, request)
        new_email = validated_data.get('email')
        customer = Customer.objects.get(id=request.auth.payload.get('user_id'))
        if new_email == customer.email:
            return Response({'msg': f'{new_email} is your current email'})
        if is_email_has_been_used(new_email):
            return Response({'msg': 'Email is already used'})
        
        expiry_date = timezone.now() + timedelta(minutes=30)
        verify_code = uuid.uuid4()
        code = UpdateEmailVerifyCode(
            current_email=customer.email,
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


class VerifyChangeEmail(APIView):
    permission_classes = (IsAuthenticated, )

    # body: {verify_code, request_id} where id is UpdateEmailCode's id
    # Response: {msg}
    
    def post(self, request):
        validated_data = get_validated_data(VerifyUpdateEmailSerializer, request)
        try:
            with transaction.atomic():
                code = UpdateEmailVerifyCode.objects.get(id=validated_data.get('request_id'))
                if timezone.now() > code.expiry_date:
                    code.delete()
                    return Response({'msg': 'The verify code has been expired.'})
                if is_email_has_been_used(code.new_email):
                    code.delete()
                    return Response({'msg': 'Email is already used.'})
                customer = Customer.objects.get(id=request.auth.payload.get('user_id'))
                customer.email = code.new_email
                customer.save()
                code.delete()
                return Response({'msg': 'Your email has been updated.'})
        except IntegrityError:
            return Response({'msg': 'Server error. Please try again later.'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except UpdateEmailVerifyCode.DoesNotExist:
            return Response({'msg': 'There are no current request to update email.'}, status.HTTP_400_BAD_REQUEST)



def get_validated_data(serializer, request, raise_exception=True):
    s = serializer(data=request.data)
    s.is_valid(raise_exception=raise_exception)
    return s.validated_data

def is_email_has_been_used(email):
    return Customer.objects.filter(email=email).exists()