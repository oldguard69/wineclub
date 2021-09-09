import os
import stripe
from django.db import transaction
from rest_framework import serializers

from subscription.models import Subscription
from base.helpers import initialize_dotenv
initialize_dotenv()

stripe.api_key = os.getenv('stripe_sk')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class SubscriptionCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    lookup_key = serializers.CharField()
    unit_amount = serializers.IntegerField()
    currency = serializers.CharField()
    interval = serializers.ChoiceField(choices=['month', 'year'])
    interval_count = serializers.IntegerField()
    description = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                name = validated_data.get('name')
                lookup_key = validated_data.get('lookup_key')

                product = stripe.Product.create(
                    name=name,
                    description=validated_data.get('description')
                )
                price = stripe.Price.create(
                    unit_amount=validated_data.get('unit_amount'),
                    currency=validated_data.get('currency'),
                    recurring={
                        "interval": validated_data.get('interval'),
                        "interval_count": validated_data.get('interval_count')
                    },
                    product=product.id,
                    lookup_key=lookup_key
                )
                
                sub = Subscription.objects.create(
                    name=name,
                    lookup_key=lookup_key,
                    stripe_product_id=product.id,
                    stripe_price_id=price.id
                )

                sub.save()
                return sub
        except Exception as e:
            return e

class SubscriptionUpdateSerializer(serializers.Serializer):
    name = serializers.CharField()
    lookup_key = serializers.CharField()
    description = serializers.CharField(allow_blank=True)

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                name = validated_data.get('name', instance.name)
                lookup_key = validated_data.get('lookup_key', instance.lookup_key)
                description = validated_data.get('description', instance.description)
                stripe.Product.modify(
                    instance.stripe_product_id,
                    name=name,
                    description=description
                )
                stripe.Price.modify(
                    instance.stripe_price_id,
                    lookup_key=lookup_key
                )
                instance.name = name
                instance.lookup_key = lookup_key
                instance.description = description
                instance.save()
                return instance
        except Exception as e:
            return e