from rest_framework import serializers
from .models import CustomUser
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class SignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
            "email",
        ]

    def validate(self, attrs):
        password = attrs.get("password", None)
        password_confirm = attrs.get("password_confirm", None)

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Parollar mos emas")

        if len(password) < 5:
            raise ValidationError("Parol uzunligi 5 tadan kop bolsin")

        return super().validate(attrs)

    def validate_email(self, value):
        x = value.split("@")
        if (
            "@" not in value
            or len(x[0]) < 5
            or int(len(x[1])) < 3
            or "." not in x[1][1 : len(x[1]) - 1]
        ):
            raise ValidationError("Xato email")
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")

        password = validated_data.pop("password")

        user = CustomUser.objects.create_user(**validated_data, password=password)
        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise ValidationError({"message": "Login yoki parol xato"})

        token, created = Token.objects.get_or_create(user=user)

        attrs["user"] = user
        attrs["token"] = token

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "username", "email"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
        ]

        extra_kwargs = {  # type: ignore
            "first_name": {"required": False},
            "username": {"required": False},
            "email": {"required": False},
        }

        def validate_email(self, value):

            parts = value.split("@")
            if (
                len(parts) != 2
                or len(parts[0]) < 5
                or len(parts[1]) < 3
                or "." not in parts[1][1:-1]
            ):
                raise ValidationError("Invalid email address.")
            return value.lower()

        def update(self, instance, validated_data):
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.username = validated_data.get("username", instance.username)
            instance.email = validated_data.get("email", instance.email)
            return super().update(instance, validated_data)

        def to_representation(self, instance):
            return {
                "username": instance.username,
                "first_name": instance.first_name,
                "email": instance.email,
                "message": "Profile updated successfully.",
            }


class UserChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(write_only=True, required=True)
    new_pass = serializers.CharField(write_only=True, required=True)
    conf_new_pass = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context["request"].user

        old_pass = data.get("old_pass")
        new_pass = data.get("new_pass")
        conf_new_pass = data.get("conf_new_pass")

        if not user.check_password(old_pass):
            raise ValidationError({"message": "Eski parol xato"})

        if new_pass and conf_new_pass and new_pass != conf_new_pass:
            raise ValidationError({"message": "Parollar mos emas"})

        data["user"] = user

        return data

    def save(self):
        user = self.validated_data["user"]
        new_pass = self.validated_data["new_pass"]

        user.set_password(new_pass)
        user.save()

        return user
