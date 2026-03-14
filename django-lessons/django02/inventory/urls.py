from django.urls import path
from .views import view_inventory, add_inventory, delete_medicine


urlpatters = [
    path('view-inventory/', view_inventory),
    path('add-inventory/', add_inventory),
    path('delete-medicine/', delete_medicine)
]