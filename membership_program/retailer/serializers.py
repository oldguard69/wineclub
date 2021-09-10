from django.db.models.fields import CharField
from user.models import User
from customer.models import Customer
from rest_framework import serializers


from business.retailer.serializers import BusinessProfileSerializer
from base.validators import price_validator
from membership_program.models import MembershipProgram
import base.templates.error_templates as errors

class MembershipProgramSerializer(serializers.ModelSerializer):
    business = BusinessProfileSerializer(read_only=True)
    price = serializers.FloatField(validators=[price_validator])

    class Meta:
        model = MembershipProgram
        exclude = ['customer']

    def validate_discount_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError(errors.DISCOUNT_PECENTAGE_ERROR)
        return value


class UserSerialier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class MembershipCustomerListSerializer(serializers.ModelSerializer):
    user = UserSerialier()
    
    class Meta:
        model = Customer
        fields = ['user', 'favorite_region', 'favorite_wine_type']


class CustomerIdSerializer(serializers.Serializer):
    customer_id = serializers.CharField()
