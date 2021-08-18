from django.db import IntegrityError, transaction
from rest_framework import serializers

from customer.models import Customer
from book.serializer import BookSerializer
from cart.models import Cart

class CustomerSerializer(serializers.ModelSerializer):
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
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()