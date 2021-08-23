from rest_framework import serializers

class CreatePaymentIntentSerializer(serializers.Serializer):
    currency = serializers.CharField()
    amount = serializers.FloatField()