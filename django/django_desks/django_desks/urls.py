from django.contrib import admin
from django.urls import path
from desk_controller.views import fetch_desks, desk_info, desk_state_update

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', fetch_desks, name='fetch_desks'),
    path('home/<int:desk_id>/', desk_info, name='desk'),
    path('home/<int:desk_id>/state/', desk_state_update, name='desk_category_update'),
    path('user_authentication/', include('django.contrib.auth.urls')),
    path('user_authentication/', include('user_authentication.urls')),
]
