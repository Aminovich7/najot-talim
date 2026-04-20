from django.db import models

# Create your models here.


class Watch(models.Model):
    brand_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand_name





