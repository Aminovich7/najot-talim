from django.urls import path
from .views import list_create, update_detail_destroy

urlpatterns = [

    path('list-create/', list_create),
    path('update-detail-destroy/', update_detail_destroy),

]