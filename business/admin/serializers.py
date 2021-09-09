from rest_framework import serializers

from business.models import Business
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Business
        fields = '__all__'
