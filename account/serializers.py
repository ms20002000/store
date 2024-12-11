from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'address']

    def validate_phone_number(self, value):
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already registered.")
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
