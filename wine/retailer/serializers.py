from rest_framework import serializers

from wine.models import Wine
from base.validators import price_validator, quantity_validator
from business.retailer.serializers import BusinessProfileSerializer

class WineSerializer(serializers.ModelSerializer):
    business = BusinessProfileSerializer(read_only=True)
    price = serializers.FloatField(validators=[price_validator])
    quantity = serializers.IntegerField(validators=[quantity_validator])

    class Meta:
        model = Wine
        fields = '__all__'