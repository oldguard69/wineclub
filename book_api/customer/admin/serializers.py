from rest_framework import serializers

from customer.models import Customer
from employee.admin.serializers import UserSerializer

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        exclude = ('favorite_books',)
