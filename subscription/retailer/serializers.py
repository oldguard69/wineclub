
from rest_framework import serializers


class CreateStripeSubscriptionSerializer(serializers.Serializer):
    price_id = serializers.CharField()

class CancelStripeSubscriptionSerializer(serializers.Serializer):
    subscription_id = serializers.CharField()

    