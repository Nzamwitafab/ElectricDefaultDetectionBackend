# core/apps.py
import os
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if not os.getenv('DISABLE_SIGNALS'):
            import core.signals  # Only load signals when not in manual mode