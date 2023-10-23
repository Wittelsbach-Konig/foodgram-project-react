from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from core.mixins import (
    ListAndRetrieveModelMixin,
    CSVResponseMixin,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    FavouriteList,
    ShoppingList,
    IngredientQuantity,
)
from api.serializers.recipe_serializers import (
    RecipeSerializer,
)
from api.serializers.compact_recipe_serializers import (
    IngredientSerializer,
    CompactRecipeSerializer,
    FavouriteListSerializer,
    ShoppingListSerializer,
    TagSerializer,
)
from api.filters import (
    IngredientFilterSet,
    RecipeFilterSet,
)
from core.permissions import IsAuthorOrAdminOrReadOnly


class TagViewSet(ListAndRetrieveModelMixin):
    """ViewSet для регистрации пользователей.

    Args:
        ListAndCreateModelMixin (type): Кастомный viewset, доступен метод GET.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListAndRetrieveModelMixin):
    """ViewSet для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet


class RecipeViewSet(viewsets.ModelViewSet,
                    CSVResponseMixin):
    """ViewSet для рецептов, список покупок и избранного."""

    queryset = (Recipe.objects.select_related('author')
                .prefetch_related('tag', 'ingredients').all())
    permission_classes = (
        IsAuthorOrAdminOrReadOnly,
    )
    filterset_class = RecipeFilterSet
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=('get',),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self):
        """Загрузка списка покупок."""
        ingredient_list = (
            IngredientQuantity.objects.filter(
                recipe__shopping_list__user=self.request.user
            ).values(
                'ingredient__name',
                'ingredient__measurement_unit',
            ).order_by(
                'ingredient__name',
            ).annotate(sum=Sum('amount'))
        )
        data = [
            {
                'Ингредиент': item['ingredient__name'],
                'Единица измерения': item['ingredient__measurement_unit'],
                'Количество': item['sum']
            }
            for item in ingredient_list
        ]
        filename = "shopping_list.csv"
        return self.render_to_csv_response(data, filename)

    def abstract_post_delete_action(self, custom_serializer, model):
        """Абстрактный action для POST, DELETE методов."""
        recipe = get_object_or_404(Recipe, id=self.kwargs.get("recipe_id"))
        if self.request.method == 'POST':
            serializer = custom_serializer(
                data={
                    'user': self.request.user.id,
                    'recipe': recipe.pk,
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            compact_recipe_serializer = CompactRecipeSerializer(recipe)
            return Response(
                compact_recipe_serializer.data,
                status=status.HTTP_201_CREATED,
            )
        model_recipe = get_object_or_404(
            model,
            user=self.request.user,
            recipe=recipe,
        )
        model_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self):
        """Добавление/Удаление рецептов в списке покупок."""
        self.abstract_post_delete_action(ShoppingListSerializer,
                                         ShoppingList)
        # recipe = get_object_or_404(Recipe, id=self.kwargs.get("recipe_id"))
        # if self.request.method == 'POST':
        #     serializer = ShoppingListSerializer(
        #         data={
        #             'user': self.request.user.id,
        #             'recipe': recipe.pk,
        #         }
        #     )
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     compact_recipe_serializer = CompactRecipeSerializer(recipe)
        #     return Response(
        #         compact_recipe_serializer.data,
        #         status=status.HTTP_201_CREATED,
        #     )
        # shopping_cart_recipe = get_object_or_404(
        #     ShoppingList,
        #     user=self.request.user,
        #     recipe=recipe,
        # )
        # shopping_cart_recipe.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=('post', 'delete'),
        url_path='favorite',
        url_name='favorite',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self):
        """Добавление/Удаление рецептов в избранном."""
        self.abstract_post_delete_action(FavouriteListSerializer,
                                         FavouriteList)
        # recipe = get_object_or_404(Recipe, id=self.kwargs.get("recipe_id"))
        # if self.request.method == 'POST':
        #     serializer = FavouriteListSerializer(
        #         data={
        #             'user': self.request.user.id,
        #             'recipe': recipe.pk,  # id
        #         }
        #     )
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     compact_recipe_serializer = CompactRecipeSerializer(recipe)
        #     return Response(
        #         compact_recipe_serializer.data,
        #         status=status.HTTP_201_CREATED,
        #     )
        # favorite_recipe = get_object_or_404(
        #     FavouriteList,
        #     user=self.request.user,
        #     recipe=recipe,
        # )
        # favorite_recipe.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
