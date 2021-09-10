from rest_framework import serializers
from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework.exceptions import ValidationError
import stripe
import os

from business.models import Business
from base.helpers import initialize_dotenv
initialize_dotenv()

stripe.api_key = os.getenv('stripe_sk')

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['email', 'adress', 'phone', 'business_category']


class BusinessCreateSerializer(serializers.ModelSerializer):
    payment_method = serializers.CharField()

    class Meta:
        model = Business
        fields = ['email', 'address', 'phone', 'payment_method', 'business_category']

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = validated_data.pop('user')
                payment_method_id = validated_data.pop('payment_method')
                user.is_retailer = True
                user.save()

                stripe_customer = stripe.Customer.create(
                    email=validated_data.get('email')
                )

                business = Business.objects.create(
                    user=user,
                    email=validated_data.get('email'),
                    phone=validated_data.get('phone'),
                    address=validated_data.get('address'),
                    business_category=validated_data.get('business_category'),
                    stripe_customer_id=stripe_customer['id'],
                )
                business.save()

                # attach payment method
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=stripe_customer['id']
                )
                
                return business
        except Exception as e:
            raise ValidationError(str(e))


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        exclude = ['user', 'subscription']
        read_only_fields = ['stripe_customer_id', 'stripe_subscription_id', 'stripe_account_id']

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                print(validated_data)
                instance.phone = validated_data.get('phone', instance.phone)
                instance.address = validated_data.get('address', instance.address)
                instance.business_category = validated_data.get('business_category', instance.business_category)
                instance.email = validated_data.get('email', instance.email)
                instance.save()
                return instance
        except IntegrityError:
            return 'error'