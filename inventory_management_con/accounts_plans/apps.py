from django.apps import AppConfig


class AccountsPlansConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts_plans"

    def ready(self):
        import accounts_plans.signals