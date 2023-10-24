from rest_framework import serializers

from recipes.models import Recipe
from core.field_mixins import CustomBase64ImageFieldMixin


class CompactRecipeSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для рецептов.
    Для избранного/списка покупок.
    """

    image = CustomBase64ImageFieldMixin()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        read_only_fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
