from rest_framework import serializers
from django.db import transaction
from django.db.utils import IntegrityError


from user.models import User
from customer.models import Customer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        read_only_fields = ['email']

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'reward_points', 'favorite_region', 'favorite_wine_type']

    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                user_data = validated_data.pop('user')
                user = instance.user
                instance.favorite_region = validated_data.get('favorite_region', instance.favorite_region)
                instance.favorite_wine_type = validated_data.get('favorite_wine_type', instance.favorite_wine_type)
                instance.save()

                user.first_name = user_data.get('first_name', user.first_name)
                user.last_name = user_data.get('last_name', user.last_name)
                user.phone = user_data.get('phone', user.phone)
                user.address = user_data.get('address', user.address)
                user.save()
                return instance
        except IntegrityError:
            return 'error'

class FavoriteWineTypeSerializer(serializers.Serializer):
    favorite_wine_type = serializers.CharField()

    def update(self, instance, validated_data):
        instance.favorite_wine_type = validated_data.get('favorite_wine_type')
        instance.save()
        return instance

class FavoriteRegionSerializer(serializers.Serializer):
    favorite_region = serializers.CharField()

    def update(self, instance, validated_data):
        instance.favorite_region = validated_data.get('favorite_region')
        instance.save()
        return instance