from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone
from .models import CustomUser
from django.core.mail import send_mail
from django.conf import settings

logger = get_task_logger(__name__)


@shared_task
def send_welcome_email(user_id, username):
    """Yangi foydalanuvchi ro'yxatdan o'tganda xabar yuborish."""
    send_mail(
        subject="Xush kelibsiz!",
        message=f"Hurmatli {username}, bizning blogga xush kelibsiz!",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@blog.uz"),
        recipient_list=["admin@blog.uz"],
        fail_silently=True,
    )
    logger.info(f"Welcome email sent for user {username} (id={user_id})")


@shared_task
def check_premium_expiry():
    """Premium muddati tugagan foydalanuvchilarni tekshirish."""


    expired_users = CustomUser.objects.filter(
        is_premium=True,
        premium_expires_at__lte=timezone.now(),
    )
    count = expired_users.update(is_premium=False)
    logger.info(f"Expired premium revoked for {count} users")
    return count
