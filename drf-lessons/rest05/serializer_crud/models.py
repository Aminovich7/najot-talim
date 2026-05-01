from django.db import models

class Watch(models.Model):
    brand = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    discount = models.PositiveIntegerField(max_length=100, blank=True, default=0)
    total_price = models.DecimalField(max_digits=50, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args,**kwargs):
        if self.price and self.discount:
            from decimal import Decimal
            self.total_price = self.price * (1 - Decimal(self.discount) / 100)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.brand






