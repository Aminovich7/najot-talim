from django.urls import path
from .views import get_phone_list, add_phone, phone_detail, phone_delete, update_phone


urlpatterns = [
    path('', get_phone_list, name='list'),
    path('add/', add_phone, name='add'),
    path('detail/<int:id>', phone_detail, name='detail'),
    path('delete/<int:id>', phone_delete, name='delete'),
    path('update/<int:id>', update_phone, name='update')

]
