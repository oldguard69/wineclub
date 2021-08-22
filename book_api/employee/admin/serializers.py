from django.db import transaction
from django.db.utils import IntegrityError
from rest_framework import serializers


from employee.models import Employee
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Employee
        fields = '__all__'

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user_data = validated_data.pop('user')
                password = user_data.pop('password')
                user = User.objects.create(**user_data)
                user.set_password(password)
                user.save()
                employee = Employee.objects.create(user=user, **validated_data)
                employee.save()
                return employee
        except IntegrityError:
            return 'error'