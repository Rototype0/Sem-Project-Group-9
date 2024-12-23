from django.contrib import admin
from desk_controller.models import *

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'name')
    search_fields = ('name',)
