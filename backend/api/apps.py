from django.apps import AppConfig


class ApiConfig(AppConfig):
    """Описание настроек приложения для api."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    verbose_name = 'апи'
