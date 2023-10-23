from django.shortcuts import get_object_or_404
from rest_framework.serializers import ValidationError
from rest_framework import status
from django.conf import settings

from recipes.models import Tag, Ingredient
from users.models import Subscription
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
    unique_ingredients = []
    for item in ingredients:
        ingredient = get_object_or_404(Ingredient, id=item.get('id'))
        if int(item.get('amount')) < 1:
            raise ValidationError(
                {'ingredients': ['Количество ингредиента '
                                 ' должно быть больше или равно 1.']}
            )
        if ingredient in unique_ingredients:
            raise ValidationError(
                {'ingredients': ['Ингредиенты должны быть уникальными.']}
            )
        unique_ingredients.append(ingredient)
    # if not (Ingredient.objects.filter(name__in=unique_ingredients).count()
    #         == len(unique_ingredients)):
    #     raise ValidationError(
    #             {'ingredients': ['Ингредиента не существует.']}
    #         )
    return ingredients


class ValidateRecipeMixin():

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
                {
                    'text': [
                        ("Использование запрещенных слов не допустимо. "
                         "Ну и ну вы разочаровали партию. "
                         "-10000 социального рейтинга.")
                    ]
                }
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


def validate_subscription(author, user):
    if author == user:
        return {
            "errors": "Нельзя подписываться на самого себя",
            "status": status.HTTP_400_BAD_REQUEST,
        }
    if Subscription.objects.filter(user=user, author=author).exists():
        return {
            "errors": "Подписка уже оформлена",
            "status": status.HTTP_400_BAD_REQUEST,
        }
