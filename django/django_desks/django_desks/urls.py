from django.contrib import admin
from django.urls import path
from desk_controller.views import fetch_desks, desk_info

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fetch_desks, name='fetch_desks'),
    path('<int:desk_id>/', desk_info, name='desk'),
]
