from django.urls import path
from . import views

app_name = "QRcode"

urlpatterns = [
    path("", views.home, name="Home"),
]