from rest_framework import serializers
from .models import Blog, Comment
from rest_framework.exceptions import ValidationError


class CreateBlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = ["title", "text"]

    def validate_title(self, value):
        if Blog.objects.filter(title=value).exists():
            raise ValidationError("Bunaqa nomli title bor")
        return value


class BlogDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Blog
        fields = ["author", "title", "text", "created_at"]


class UpdateBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "author",
            "title",
            "text",
        ]

        # pasdagi kodlar kerakmas chunki viewda patch ishlatdim
        # extra_kwargs = {  # type: ignore
        #     "author": {"required": False},
        #     "title": {"required": False},
        #     "text": {"required": False},
        # }

    # def update(self, instance, validated_data):

    #     # kerakmas ekan, super().update ozi qivorarkan bu ishni avtomati
    #     # instance.author = validated_data.get("author", instance.author)
    #     # instance.title = validated_data.get("title", instance.title)
    #     # instance.text = validated_data.get("text", instance.text)

    #     return super().update(instance, validated_data)

    def to_representation(self, instance):
        return {
            "author": instance.username,
            "title": instance.title,
            "text": instance.text,
            "message": "Blog updated successfully!",
        }


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["title", "text"]


class UpdateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["title", "text"]

        # pasdagi kod kerakmas chunki viewda patch ishlatdim

        # extra_kwargs = {
        #     "title": {"required": False},
        #     "text": {"required": False},
        # }

    # def update(self, instance, validated_data):
    #     return super().update(instance, validated_data)


