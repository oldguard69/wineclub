from rest_framework import serializers


from reward_program.models import RewardProgram
from business.retailer.serializers import BusinessProfileSerializer
from base.validators import reward_points_validator
import base.templates.error_templates as errors

class RewardProgramSerialzier(serializers.ModelSerializer):
    business = BusinessProfileSerializer(read_only=True)
    reward_points = serializers.IntegerField(validators=[reward_points_validator])

    class Meta:
        model = RewardProgram
        fields = '__all__'
        read_only_fields = ['reward_code']

    def validate(self, data):
        if data['start_date'] > data['expiry_date']:
            raise serializers.ValidationError(errors.END_DATE_ST_START_DATE)
        if data['total_amount'] == 0 and data['total_wine_purchased'] == 0:
            raise serializers.ValidationError(errors.AMOUNT_AND_WINE_PURCHASED_EQ_0)
        return data
    
    def validate_total_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(errors.TOTAL_WINE_PURCHASED_LT_0)
        return value

    def validate_total_wine_purchased(self, value):
        if value < 0:
            raise serializers.ValidationError(errors.TOTAL_AMOUNT_LT_0)
        return value