from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email', 'password', 'password_confirm']

    def validate_email(self, value):
        parts = value.split('@')
        if (
            len(parts) != 2
            or len(parts[0]) < 5
            or len(parts[1]) < 3
            or '.' not in parts[1][1:-1]
        ):
            raise ValidationError("Invalid email address.")
        return value.lower()  # normalize to lowercase

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise ValidationError({"password": "Passwords do not match."})

        if len(password) < 5:
            raise ValidationError({"password": "Password must be at least 5 characters."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data, password=password)
        return user

    def to_representation(self, instance):
        return {
            "username": instance.username,
            "first_name": instance.first_name,
            "message": "User created successfully.",
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'username', 'email']
        extra_kwargs = {
            'first_name': {'required': False},
            'username':   {'required': False},
            'email':      {'required': False},
        }

    def validate_email(self, value):
        parts = value.split('@')
        if (
            len(parts) != 2
            or len(parts[0]) < 5
            or len(parts[1]) < 3
            or '.' not in parts[1][1:-1]
        ):
            raise ValidationError("Invalid email address.")
        return value.lower()

    def to_representation(self, instance):
        return {
            "username":   instance.username,
            "first_name": instance.first_name,
            "email":      instance.email,
            "message":    "Profile updated successfully.",
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'username', 'email']