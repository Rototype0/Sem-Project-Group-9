from django.contrib import admin
from desk_controller.models import *

@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'name', 'latest_state')
    search_fields = ('name',)

    def latest_state(self, obj):
        if obj.state_data:
            latest = obj.state_data[-1]
            return f"Position: {latest['position_mm']} mm at {latest['timestamp']}"
        return "No data"
