from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from django.conf import settings

from recipes.models import Tag, Ingredient
from obsceneLang.utils import (
    get_words_from_text,
    get_forbidden_words,
    text_has_forbidden_words
)


def validate_tags(value):
    """Валидация тегов."""
    if not value:
        raise ValidationError(
            {'tags': ['Обязательное поле.']}
        )
    if len(value) != len(set(value)):
        raise ValidationError(
            {'tags': ['Теги должны быть уникальными.']}
        )
    if len(value) < 1:
        raise ValidationError(
            {'tags': ['Хотя бы один тег должен быть указан.']}
        )
    for tag in value:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError(
                {'tags': ['Тег несуществует.']}
            )
    return value


def validate_ingredients(ingredients):
    """Валидация ингредиентов."""
    if not ingredients:
        raise ValidationError(
            {'ingredients': ['Обязательное поле.']}
        )
    unique_ingredients = set()
    for item in ingredients:
        id = item.get('id')
        if id in unique_ingredients:
            raise ValidationError("Ингредиенты должны быть уникальными.")
        unique_ingredients.add(id)
    return ingredients


class ValidateRecipeMixin():
    """Кастомный миксин для валидации оставшихся полей рецепта."""

    def validate_image(self, value):
        """Валидация картинки."""
        if not value:
            raise ValidationError(
                {'image': ['Обязательное поле.']}
            )
        return value

    def validate_text(self, value):
        """Валидация текста."""
        if not value:
            raise ValidationError(
                {'ingredients': ['Обязательное поле.']}
            )
        forbidden_words = get_forbidden_words()
        text_words = get_words_from_text(value)
        if text_has_forbidden_words(text_words,
                                    forbidden_words,
                                    settings.THRESHOLD):
            raise ValidationError(
                ("Использование запрещенных слов не допустимо. "
                 "Ну и ну, вы разочаровали партию. "
                 "-10000 социального рейтинга ☹️📉👎.")
            )
        return value

    def validate_cooking_time(self, value):
        """Валидация времени приготовления."""
        if not value:
            raise ValidationError(
                {'cooking_time': ['Обязательное поле.']}
            )
        if int(value) < 1:
            raise ValidationError(
                {'cooking_time': ['Минимальное время = 1'], }
            )
        return value
