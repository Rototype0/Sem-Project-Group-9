from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name = 'dashboard'),
    path('charts', views.charts, name = 'charts'),
    path('modes', views.modes, name = 'modes'),
    path('profile', views.profile, name = 'profile')
]