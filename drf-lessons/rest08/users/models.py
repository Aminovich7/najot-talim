from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.username