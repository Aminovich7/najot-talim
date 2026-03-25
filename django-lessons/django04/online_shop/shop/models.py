from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name="Kategoriya"
    )
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx (so'm)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Ombordagi miqdor")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Rasm")
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def formatted_price(self):
        return f"{self.price:,.0f}"
