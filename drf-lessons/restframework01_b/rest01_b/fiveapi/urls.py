from django.urls import path
from .views import *

urlpatterns = [

    path('list/', get_list),
    path('create/', create),
    path('update-put/', update_put),
    path('update-patch/', update_patch),
    path('delete/', delete),

]