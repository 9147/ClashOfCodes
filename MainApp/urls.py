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
    path('submission/<track>', views.submission, name='submission'),
    path('logout/', views.logout_user, name='logout'),
    path('user/', views.user_view, name='user'),
    path('update_landing_page/', views.update_landing_page, name='update_landing_page'),
    path('generateReferral/', views.generateReferralCode, name='generateReferral'),
    path('referralvalidation/', views.referralValidation, name='referralValidation'),
    path('discount/', views.discount, name='discount'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('add_github_link/', views.save_github_url, name='save_github_link'),
]