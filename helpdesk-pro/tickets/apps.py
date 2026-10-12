from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tickets"
    verbose_name = "IT support"

    def ready(self):
        from .signals import register_signals

        register_signals(self)
