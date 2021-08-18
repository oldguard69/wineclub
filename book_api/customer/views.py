from customer.serializer import LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


from customer.models import Customer
from customer.serializer import CustomerSerializer


# Create your views here.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated, )

    # token carry from 
    def get(self, request, *args, **kwargs):
        validated_token = request.auth
        print(validated_token.payload)
        return self.list(request, *args, **kwargs)


class Login(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            validated_data = serializer.validated_data
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
                    status.HTTP_401_UNAUTHORIZED
                )


class Register(APIView):
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data    
            try:
                customer = Customer.objects.get(email=data.get('email'))
                return Response({'msg': 'Email has been used'}, status.HTTP_200_OK)
            except Customer.DoesNotExist:
                hash_pw = make_password(data.get('password'))
                data["password"] = hash_pw
                result = serializer.create(data)
                if result == 'error':
                    return Response(
                        data={'msg': 'Server error. Please try again later'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                return Response({'msg': 'Account created successfully'}, status.HTTP_200_OK)

