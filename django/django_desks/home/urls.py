from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.about, name='about'), 
    path('dashboard/', views.dashboard, name='dashboard'),  
]

