from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """Описание настроек приложения для рецептов, тегов, ингредиентов."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = 'Рецепты'
