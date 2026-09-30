from rest_framework import serializers
from .models import Post, Category, Comment
from users.serializers import ProfileSerializer
from django.utils import timezone

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ["name"]

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError(
                "Kategoriya nomi kamida 2 ta belgidan iborat bo'lishi kerak."
            )
        
        if not value.isalpha():
            raise serializers.ValidationError("Kategoriya nomi faqat harflardan iborat bo'lsin")
        return value



class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "author", "text", "created_at"]
        read_only_fields = ["id", "author", "created_at"]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Comment
        fields = ["text"]

    def validate_text(self, value):
        value = value.strip()
        
        if len(value) > 1000:
            raise serializers.ValidationError(
                "Izoh 1000 ta belgidan oshmasligi kerak."
            )
        return value


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True) 
    comments_count = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "author", "category",
            "title", "content", "comments",
            "is_premium", "comments_count",
            "created_at", "updated_at",
        ]
        read_only_fields = fields

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_content(self, obj):
        if not obj.is_premium:
            return obj.content

        request = self.context.get("request")
        if request and request.user.is_authenticated and request.user.is_premium_active:
            return obj.content

        preview = obj.content[:200]
        return f"{preview}… To'liq o'qish uchun premium obuna kerak."


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model  = Post
        fields = ["title", "content", "category", "is_premium"]


 
    def validate_is_premium(self, value):
        request = self.context.get("request")
        if value and request and not request.user.is_premium:
            raise serializers.ValidationError(
                "Faqat premium obunasi bor kishilar premium post yarata oladi."
            )
        return value


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Post
        fields = ["title", "content", "category"]
        extra_kwargs = {field: {"required": False} for field in fields}

