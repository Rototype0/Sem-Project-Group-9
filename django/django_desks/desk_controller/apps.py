from django.apps import AppConfig


class DeskControllerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'desk_controller'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()
