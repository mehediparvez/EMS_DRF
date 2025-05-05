from rest_framework import serializers
from apps.users.models import Employer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ('id', 'company_name', 'contact_person_name', 'email', 
                  'phone_number', 'address', 'created_at')
        read_only_fields = ('id', 'created_at')
    
    def create(self, validated_data):
        # Automatically set the user to the current authenticated user
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)