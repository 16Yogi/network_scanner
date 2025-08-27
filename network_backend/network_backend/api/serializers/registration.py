from rest_framework import serializers
from api.models.registration import UserRegistration
from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = ['fullname','email','password']
    
    def create(self,validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return UserRegistration.objects.create(**validated_data)