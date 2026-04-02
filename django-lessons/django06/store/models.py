from django.db import models


class Phone(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    storage = models.IntegerField()
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.brand} {self.model}"