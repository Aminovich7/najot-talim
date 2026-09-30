from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    year = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.first_name