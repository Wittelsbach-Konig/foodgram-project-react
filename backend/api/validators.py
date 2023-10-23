from rest_framework.serializers import ValidationError
from django.conf import settings

from recipes.models import Tag
from obsceneLang.utils import (
    get_words_from_text,
    get_forbidden_words,
    text_has_forbidden_words
)


def validate_tags(data):
    """Валидация тегов."""
    if not data:
        raise ValidationError(
            {'tags': ['Обязательное поле.']}
        )
    if len(data) != len(set(data)):
        raise ValidationError(
            {'tags': ['Теги должны быть уникальными.']}
        )
    if len(data) < 1:
        raise ValidationError(
            {'tags': ['Хотя бы один тег должен быть указан.']}
        )
    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError(
                {'tags': ['Тег несуществует.']}
            )
    return data


def validate_ingredients(data):
    """Валидация ингредиентов."""
    if not data:
        raise ValidationError(
            {'ingredients': ['Обязательное поле.']}
        )
    return data


def validate_text(data: str):
    """Валидация текста."""
    if not data:
        raise ValidationError(
            {'ingredients': ['Обязательное поле.']}
        )
    forbidden_words = get_forbidden_words()
    text_words = get_words_from_text(data)
    if text_has_forbidden_words(text_words,
                                forbidden_words,
                                settings.THRESHOLD):
        raise ValidationError(
            {
                'text': [
                    ("Использование запрещенных слов не допустимо. "
                     "Ну и ну вы разочаровали партию. "
                     "-10000 социального рейтинга.")
                ]
            }
        )
    return data


def validate_cooking_time(data):
    """Валидация времени приготовления."""
    if not data:
        raise ValidationError(
            {'cooking_time': ['Обязательное поле.']}
        )
    if int(data) < 1:
        raise ValidationError(
            {'cooking_time': ['Минимальное время = 1'], }
        )
    return data
