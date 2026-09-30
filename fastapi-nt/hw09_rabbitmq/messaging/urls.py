from django.urls import path

from messaging import views


urlpatterns = [
    path("", views.home, name="home"),
    path("publish/", views.publish_message_view, name="publish_message"),
    path("consume/", views.consume_message_view, name="consume_message"),
]
