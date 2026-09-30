from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import decimal




class CustomUser(AbstractUser):
    profession = models.CharField(max_length=50)
    is_premium = models.BooleanField(default=False)
    premium_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username
    
    @property
    def is_premium_active(self):
        return (self.is_premium and 
                self.premium_expires_at and 
                self.premium_expires_at > timezone.now())


class Wallet(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name="Foydalanuvchi"
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=decimal.Decimal("0.00"),
        verbose_name="Balans"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hamyon"
        verbose_name_plural = "Hamyonlar"

    def __str__(self):
        return f"{self.user.username} — {self.balance} UZS"


@receiver(post_save, sender=CustomUser)
def create_wallet_for_new_user(sender, instance, created, **kwargs):
    """Yangi user yaratilganda avtomatik bo'sh hamyon ochiladi."""
    if created:
        Wallet.objects.create(user=instance)