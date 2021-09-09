from rest_framework import serializers


from business.admin.serializers import BusinessSerializer
from wine.models import Wine

class WineSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()

    class Meta:
        model = Wine
        fields = '__all__'