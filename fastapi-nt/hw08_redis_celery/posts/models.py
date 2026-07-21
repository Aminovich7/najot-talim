from django.db import models
from users.models import CustomUser
from django.utils.text import slugify



class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Kategoriya nomi"
    )
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]


    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Muallif"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="Kategoriya"
    )
    title = models.CharField(max_length=255, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    is_premium = models.BooleanField(
        default=False,
        verbose_name="Premium kontent"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ["-created_at"]

    def __str__(self):
        "Premium content" if self.is_premium else "Ommaviy content"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Post"
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Muallif"
    )
    text = models.TextField(verbose_name="Izoh matni")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Izoh"
        verbose_name_plural = "Izohlar"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author.username} | {self.post.title}"