from django.db import transaction
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import serializers

from recipes.models import (
    Recipe,
    Ingredient,
    IngredientQuantity,
)
from core.validators import (
    ValidateRecipeMixin,
    validate_tags,
    validate_ingredients,
)
from obsceneLang.validators import validate_no_obscenities
from core.mixins import (
    GetRecipe,
    GetFavorites,
    GetShoppingList,
)
from api.serializers.users_serializers import UserSerializer
from core.field_mixins import CustomBase64ImageFieldMixin
from api.serializers.compact_recipe_serializers import (
    TagSerializer,
    IngredientQuantitySerializer,
)


class RecipeSerializer(serializers.ModelSerializer,
                       GetRecipe,
                       GetFavorites,
                       GetShoppingList,
                       ValidateRecipeMixin):
    """Сериалайзер для рецептов."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientQuantitySerializer(
        read_only=True,
        many=True,
        source="ingredient_quantity"
    )
    name = serializers.CharField(
        max_length=settings.RECIPE_NAME_MAX_LENGTH,
        validators=(validate_no_obscenities,)
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    image = CustomBase64ImageFieldMixin()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def make_tags(self, instance, tags):
        """Добавление тегов к рецепту."""
        instance.tags.set(tags)

    @transaction.atomic
    def make_ingredients(self, instance, valid_ingredients):
        """Добавление ингредиентов к рецепту."""
        objects = []
        print(valid_ingredients)
        print(type(valid_ingredients))
        for data in valid_ingredients:
            amount = data.get('amount')
            ingredients = get_object_or_404(Ingredient, id=data.get('id'))
            objects.append(
                IngredientQuantity(
                    recipe=instance,
                    ingredients=ingredients,
                    amount=amount,
                )
            )
        IngredientQuantity.objects.bulk_create(objects)

    @transaction.atomic
    def create(self, validated_data):
        """Создание рецепта - POST."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        self.make_tags(recipe, tags)
        self.make_ingredients(recipe, ingredients)
        return recipe

    def validate(self, data):
        """Валидация полей при создании рецепта."""
        ingredients = self.initial_data.get('ingredients')
        validated_ingredients = validate_ingredients(ingredients)
        data['ingredients'] = validated_ingredients

        tags = self.initial_data.get('tags')
        validated_tags = validate_tags(tags)
        data['tags'] = validated_tags

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновление рецепта - PATCH."""
        instance.tags.clear()
        tags = validated_data.pop('tags')
        self.make_tags(instance, tags)

        IngredientQuantity.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        self.make_ingredients(instance, ingredients)
        return super().update(instance, validated_data)
