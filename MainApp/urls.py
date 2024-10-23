from django.urls import path
from . import views

app_name = "MainApp"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register"),
    path("login/", views.loginPage, name="login"),
    path('activate/<uidb64>/<token>/', views.activate_user, name='activate_user'),
    path('create-team/', views.create_team, name='create_team'),
    path('contact/', views.contactview, name='contact'),
    path('get_form_closing_time/', views.get_form_closing_time, name='get_form_closing_time'),
    path('submission/', views.submission, name='submission'),
]