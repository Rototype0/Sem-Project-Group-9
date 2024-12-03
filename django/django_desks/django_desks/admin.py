from django.contrib import admin

class DeskAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'name')
    search_fields = ('name')
