from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import CustomUser, Wallet
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth.hashers import check_password



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name", "profession", "password", "password_confirm"]
        extra_kwargs = {
            "email": {"required": True}
        }

    def validate_email(self, value):
        parts = value.split('@')
        if (
            len(parts) != 2
            or len(parts[0]) < 5
            or len(parts[1]) < 3
            or '.' not in parts[1][1:-1]
        ):
            raise ValidationError("Email xato! ")
        return value.lower()
    

    def validate_first_name(self, value):
        if len(value) < 3:
            raise ValidationError("Ism kamida 3-ta harf bolsin! ")
        
        if not value.isalpha():
            raise ValidationError("Ism faqat harflardan iborat bo'lsin")
        
        return value.title()
    
    def validate_last_name(self, value):
        if len(value) < 3:
            raise ValidationError("Familiya kamida 3-ta harf bolsin! ")
        
        if not value.isalpha():
            raise ValidationError("Familiya faqat harflardan iborat bo'lsin")
        
        return value.title()

    def validate(self, attrs):
        if attrs["password"] and attrs["password_confirm"] and attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password_confirm": "Parollar mos kelmadi."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")

        user = CustomUser(**validated_data)
        user.set_password(password)   
        user.save()                   
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Username yoki parol noto'g'ri.")


        attrs["user"] = user
        return attrs


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance", "updated_at"]


class ProfileSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id", "username", "email",
            "first_name", "last_name", 
            "profession",
            "is_premium",
            "wallet"
            ]
        read_only_fields = fields


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name",
            "email", "profession"
        ]
        extra_kwargs = {
            "email": {"required": False},
        }

       


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={"input_type": "password"}
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise ValidationError("Eski parol noto'g'ri.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise ValidationError({"new_password_confirm": "Yangi parollar mos kelmadi."})

        if attrs["old_password"] == attrs["new_password"]:
            raise ValidationError({"new_password": "Yangi parol eski paroldan farq qilishi kerak."})

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
    

class AccountDeleteSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Parol noto'g'ri.")
        return value
    

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1)