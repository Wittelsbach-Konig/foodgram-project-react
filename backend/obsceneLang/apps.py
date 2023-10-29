from django.apps import AppConfig


class ObscenelangConfig(AppConfig):
    """Описание настроек приложения для выявления обсценной лексики."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obsceneLang'
    verbose_name = 'Запрещённые слова'
