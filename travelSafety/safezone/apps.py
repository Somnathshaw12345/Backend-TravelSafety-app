from django.apps import AppConfig


class SafezoneConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'safezone'

    def ready(self):
        import safezone.signals
