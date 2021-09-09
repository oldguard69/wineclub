from rest_framework import serializers

from reward_program.models import RewardProgram
from business.admin.serializers import BusinessSerializer

class RewardProgramSerializer(serializers.ModelSerializer):
    business = BusinessSerializer()
    
    class Meta:
        model = RewardProgram
        fields = '__all__'