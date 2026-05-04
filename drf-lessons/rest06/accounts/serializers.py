from .models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignupSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "username", "email", "password", "password_confirm"]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password_confirm = attrs.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError({"password": "Parollar mos emas"})

        if len(password) < 5:
            raise ValidationError({"password": "Parol kamida 5ta belgidan iborat bo'lishi kerak"})

        return attrs

    def validate_email(self, value):
        if len(value) < 6:
            raise ValidationError("Email juda qisqa")
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = CustomUser.objects.create_user(**validated_data)
        return user