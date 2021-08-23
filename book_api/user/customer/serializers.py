from rest_framework import serializers
from django.db import transaction
from django.db.utils import IntegrityError
import stripe

from user.models import User
from customer.models import Customer
from cart.models import Cart
from book_api import config

stripe.api_key = config.stripe_sk

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'address', 'phone_number']

    def create(self, validated_data):
        try:
            with transaction.atomic():
                password = validated_data.pop('password')
                user = User.objects.create(**validated_data)
                user.set_password(password)
                user.save()

                stripe_customer = stripe.Customer.create()
                customer = Customer.objects.create(
                    user=user, 
                    stripe_customer_id=stripe_customer['id']
                )
                customer.save()
                
                cart = Cart.objects.create(customer=customer)
                cart.save()
                return user
        except IntegrityError:
            return 'error'