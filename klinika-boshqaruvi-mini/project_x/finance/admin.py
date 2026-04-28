from django.contrib import admin
from .models import Doctor, Consultation, Surgery, Room


admin.site.register(Doctor)
admin.site.register(Consultation)
admin.site.register(Surgery)
admin.site.register(Room)
