from django.contrib.auth.models import AbstractUser
from django.db import models


class Author(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png", blank=True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"