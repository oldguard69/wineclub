
from django.db.utils import IntegrityError
from rest_framework import serializers
from django.db import transaction


from user.models import User
from cart.models import Cart
from customer.models import Customer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

# this view work for customer
# employee will get another view
class RegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'address', 'phone_number']

    def create(self, validated_data):
        try:
            with transaction.atomic():
                password = validated_data.pop('password')
                user = User.objects.create(**validated_data)
                user.set_password(password)
                user.save()
                customer = Customer.objects.create(user=user)
                customer.save()
                cart = Cart.objects.create(customer=customer)
                cart.save()
                return user
        except IntegrityError:
            return 'error'


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()


class RequestUpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyUpdateEmailSerializer(serializers.Serializer):
    verify_code = serializers.UUIDField()
    request_id = serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'phone_number']
