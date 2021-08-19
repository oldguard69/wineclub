from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from customer.models import Customer
from book.serializers import BookSerializer
from cart.models import Cart

class RegisterSerializer(serializers.ModelSerializer):
    favorite_books = BookSerializer(read_only=True, many=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                customer = Customer.objects.create(**validated_data)
                customer.save()
                cart = Cart.objects.create(total_amount=0, customer=customer)
                cart.save()
                return customer
        except IntegrityError:
            return 'error'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('password', 'favorite_books')

class CustomerProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)
    date_join = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Customer
        exclude = ('favorite_books', 'password')
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

class RequestUpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyUpdateEmailSerializer(serializers.Serializer):
    verify_code = serializers.UUIDField()
    request_id = serializers.IntegerField()