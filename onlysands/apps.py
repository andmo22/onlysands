from django.apps import AppConfig


class OnlysandsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "onlysands"

    def ready(self):
        import onlysands.signals
