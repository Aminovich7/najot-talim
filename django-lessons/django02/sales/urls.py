from django.urls import path
from .views import sell_medicine, return_medicine

urlpatterns = [

    path('sell-medicine/', sell_medicine),
    path('return-medicine/', return_medicine),
]