from django.contrib import admin
from django.urls import path
from .views import fetch_desks, desk_info

urlpatterns = [
    path('', fetch_desks, name='fetch_desks'),
    path('<int:desk_id>/', desk_info, name='desk'),
]
