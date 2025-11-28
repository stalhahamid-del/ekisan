from django.apps import AppConfig


class MyadminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myadmin'


# apps.py
from django.apps import AppConfig

class MyadminConfig(AppConfig):
    name = 'myadmin'

    def ready(self):
        import myadmin.signals  # Ensure that the signals are imported
