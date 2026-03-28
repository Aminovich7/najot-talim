from django.db import models

class Phone(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    color = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    

    # class Meta: 
    #     verbose_name = 'phone'
    #     db_table = 'phones_list'

    def __str__(self):
        return f"{self.brand} {self.model}"
    

    