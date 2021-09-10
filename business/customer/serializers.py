from rest_framework import serializers


from business.models import Business
from business_category.models import BusinessCategory

class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    business_category = BusinessCategorySerializer()
    
    class Meta:
        model = Business
        fields = ['email', 'address', 'phone', 'business_category']