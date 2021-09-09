from rest_framework import serializers


def reward_points_validator(value):
    if value < 0:
        raise serializers.ValidationError('Reward points must greater than or equal to 0.')

def price_validator(value):
    if value <= 0:
        raise serializers.ValidationError('Price must greater than 0.')

def quantity_validator(value):
    if value <= 0:
        raise serializers.ValidationError('Quantity must greater than 0.')
    
