from rest_framework import serializers


from business.admin.serializers import BusinessSerializer
from tourism_pass.models import TourismPass

class TourismPassSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()

    class Meta:
        model = TourismPass
        fields = '__all__'