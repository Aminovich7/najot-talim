from django.db import models

class Watch(models.Model):
    name = models.CharField(max_length=100)
    price      = models.DecimalField(max_digits=10, decimal_places=2)
    country    = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name