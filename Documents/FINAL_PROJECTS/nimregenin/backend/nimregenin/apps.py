from django.apps import AppConfig

class NimregeninConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nimregenin'

    def ready(self):
        import nimregenin.signals  # noqa: F401 - This imports and registers the signals
