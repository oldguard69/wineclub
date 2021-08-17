from rest_framework import generics
from rest_framework_simplejwt.tokens import Token, AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from book_api.settings import SECRET_KEY
from customer.models import Customer
from customer.serializer import CustomerSerializer

def get_access_token(request):
    jwt_object = JWTAuthentication() 
    header = jwt_object.get_header(request)
    raw_token = jwt_object.get_raw_token(header)
    print(request.auth.payload)
    validated_token = jwt_object.get_validated_token(raw_token)
    return validated_token

# Create your views here.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # token carry from 
    def get(self, request, *args, **kwargs):
        validated_token = get_access_token(request)
        
        # print(validated_token.payload)
        # payload = jwt.decode(
        #     validated_token.encode(),
        #     SECRET_KEY,
        #     algorithms=['HS256'],
        # )
        # print(payload)
        return self.list(request, *args, **kwargs)
