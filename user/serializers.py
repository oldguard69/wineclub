from rest_framework import serializers
from user.models import ResetPasswordCode
from datetime import timedelta
from django.utils import timezone
import uuid


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance


class RequestUpdateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyUpdateEmailSerializer(serializers.Serializer):
    verify_code = serializers.UUIDField()
    request_id = serializers.IntegerField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        expiry_date = timezone.now() + timedelta(minutes=30)
        verify_code = uuid.uuid4()
        print(verify_code)
        code = ResetPasswordCode.objects.create(
            email=validated_data.get('email'),
            verify_code=verify_code,
            expiry_date=expiry_date
        )
        code.save()
        return code

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    verify_code = serializers.UUIDField()

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('new_password'))
        instance.save()
        return instance