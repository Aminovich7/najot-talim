from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password", "password_confirm"]
    
    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("First name must be at least 3 characters long.")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value.title()

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value.title()

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return value.lower()
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]

    def validate_first_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("First name must be at least 3 characters long.")
        if not value.isalpha():
            raise serializers.ValidationError("First name must contain only letters.")
        return value.title()

    def validate_last_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long.")
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")
        return value.title()

    def validate_username(self, value):
        if len(value) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return value.lower()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    new_password_conf = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_conf"]:
            raise serializers.ValidationError({"new_password_conf": "New passwords do not match."})

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({"new_password": "New password must be different from old password."})

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user