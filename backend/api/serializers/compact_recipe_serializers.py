from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from core.field_mixins import CustomBase64ImageFieldMixin
from recipes.models import (
    Tag,
    Recipe,
    Ingredient,
    FavouriteList,
    ShoppingList,
    IngredientQuantity,
)


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


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов."""

    class Meta:
        model = Tag,
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер для ингредиентов."""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit',
        )


class IngredientQuantitySerializer(serializers.ModelSerializer):
    """Сериалайзер для количества ингредиентов."""

    id = serializers.ReadOnlyField(source="ingredients.id")
    name = serializers.ReadOnlyField(source="ingredients.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredients.measurement_unit"
    )

    class Meta:
        model = IngredientQuantity
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


class FavouriteListSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка избранного."""

    class Meta:
        model = FavouriteList
        fields = (
            'user',
            'recipe',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=FavouriteList.objects.all(),
                fields=('user', 'recipe'),
            ),
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    """Сериалайзер для списка покупок."""

    class Meta:
        model = ShoppingList
        fields = (
            'user',
            'recipe',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=('user', 'recipe'),
            ),
        ]
