from django.urls import path
from ..django_desks.views import fetch_desks

urlpatterns = [
    path('fetch-desks/', fetch_desks, name='fetch_desks'),
]