from django.contrib import admin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_superuser")