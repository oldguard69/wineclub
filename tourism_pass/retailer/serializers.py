from rest_framework import serializers


from tourism_pass.models import TourismPass
from base.validators import reward_points_validator
from business.retailer.serializers import BusinessProfileSerializer
import base.templates.error_templates as errors

class TourismPassSerializer(serializers.ModelSerializer):
    business = BusinessProfileSerializer(read_only=True)
    reward_points = serializers.IntegerField(validators=[reward_points_validator])

    class Meta:
        model = TourismPass
        fields = '__all__'
        read_only_fields = ['qr_code']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(errors.PRICE_ERROR)
        return value

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError(errors.END_DATE_ST_START_DATE)
        return data