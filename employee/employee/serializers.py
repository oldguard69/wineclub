from rest_framework import serializers
from employee.models import Employee
from user.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('email', 'role', 'salary',)


class EmployeeProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'address']