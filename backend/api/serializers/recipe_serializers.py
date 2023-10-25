from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers.users_serializers import UserSerializer
from core.field_mixins import CustomBase64ImageFieldMixin
from core.mixins import GetFavorites, GetRecipe, GetShoppingList
from core.validators import (ValidateRecipeMixin, validate_ingredients,
                             validate_tags)
from obsceneLang.validators import validate_no_obscenities
from recipes.models import (FavouriteList, Ingredient, IngredientQuantity,
                            Recipe, ShoppingList, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тегов."""

    class Meta:
        model = Tag
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


class GetRecipeSerializer(serializers.ModelSerializer,
                          GetRecipe,
                          GetFavorites,
                          GetShoppingList,):
    """Сериалайзер только для чтения."""

    author = UserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientQuantitySerializer(
        read_only=True,
        many=True,
        source="ingredient_quantity"
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    image = serializers.SerializerMethodField(read_only=True)

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

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class RecipeSerializer(serializers.ModelSerializer,
                       GetRecipe,
                       #  GetFavorites,
                       #  GetShoppingList,
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
    # is_favorited = serializers.SerializerMethodField(
    #     read_only=True
    # )
    # is_in_shopping_cart = serializers.SerializerMethodField(
    #     read_only=True
    # )
    image = CustomBase64ImageFieldMixin()
    # image = serializers.SerializerMethodField(read_only=True)

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

    def make_ingredients(self, instance, valid_ingredients):
        """Добавление ингредиентов к рецепту."""
        objects = []
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

    def update(self, instance, validated_data):
        """Обновление рецепта - PATCH."""
        instance.tags.clear()
        tags = validated_data.pop('tags')
        self.make_tags(instance, tags)

        IngredientQuantity.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        self.make_ingredients(instance, ingredients)
        return super().update(instance, validated_data)

    def to_representation(self, recipe):
        """Для чтения используется GetRecipeSerializer."""
        serializer = GetRecipeSerializer(recipe)
        return serializer.data
