from django.contrib import admin
from django.urls import path
from desk_controller.views import fetch_desks, desk_info, desk_state_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', fetch_desks, name='fetch_desks'),
    path('<int:desk_id>/', desk_info, name='desk'),
    path('<int:desk_id>/state/', desk_state_update, name='desk_category_update'),
]
