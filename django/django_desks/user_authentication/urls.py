from django.urls import path
from . import views
from .views import dashboard

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name='logout'),
    path('register_user', views.register_user, name='register_user'),
    path('profile', views.profile, name = 'profile'),
    path('dashboard', dashboard, name='dashboard'),
]
