from rest_framework import serializers


from business.admin.serializers import BusinessSerializer
from membership_program.models import MembershipProgram

class MembershipProgramSerializer(serializers.ModelSerializer):
    business = BusinessSerializer
    
    class Meta:
        model = MembershipProgram
        exclude = ['customer']