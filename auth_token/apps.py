from django.apps import AppConfig


class AuthTokenConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_token"

    def ready(self) -> None:
        from auth_token import signals

        return super().ready()
