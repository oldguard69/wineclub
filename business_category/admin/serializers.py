from rest_framework import serializers

from business_category.models import BusinessCategory

class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = '__all__'