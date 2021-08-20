from employee.serializers import UserSerializer
from rest_framework import serializers

from customer.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Customer
        exclude = ('favorite_books',)
