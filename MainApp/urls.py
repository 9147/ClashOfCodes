from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = "MainApp"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_user, name="register"),
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("activate/<uidb64>/<token>/", views.activate_user, name="activate"),
    path('create-team/', views.create_team, name='create_team'),
]