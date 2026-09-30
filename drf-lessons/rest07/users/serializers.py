from rest_framework import serializers
from users.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Author
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return Author.objects.create_user(**validated_data)