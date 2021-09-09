from rest_framework import serializers
from django.db import transaction
from django.db.utils import IntegrityError
import stripe
import os


from user.models import User
from customer.models import Customer
from cart.models import Cart
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

stripe.api_key = os.getenv('stripe_sk')

class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'address', 'phone']

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