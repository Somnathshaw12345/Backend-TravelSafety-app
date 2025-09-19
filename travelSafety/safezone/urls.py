from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("emergency/", views.send_emergency, name="send_emergency"),
]
