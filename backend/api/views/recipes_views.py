from django.db.models import Sum
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from api.filters import IngredientFilterSet, RecipeFilterSet
from api.serializers.recipe_serializers import (FavouriteListSerializer,
                                                IngredientSerializer,
                                                RecipeSerializer,
                                                ShoppingListSerializer,
                                                TagSerializer,
                                                GetRecipeSerializer)
from core.mixins import ListAndRetrieveModelMixin, PDFResponseMixin
from core.pagination import CustomPagination
from core.permissions import IsAuthorOrAdminOrReadOnly
from core.utils import recipe_post_delete_action
from recipes.models import (Favourites, Ingredient, IngredientQuantity,
                            Recipe, Shopping, Tag)


class TagViewSet(ListAndRetrieveModelMixin):
    """ViewSet для регистрации пользователей.

    Args:
        ListAndCreateModelMixin (type): Кастомный viewset, доступен метод GET.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ListAndRetrieveModelMixin):
    """ViewSet для ингредиентов.

    Args:
        ListAndCreateModelMixin (type): Кастомный viewset, доступен метод GET.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet


class RecipeViewSet(viewsets.ModelViewSet,
                    PDFResponseMixin):
    """ViewSet для рецептов, список покупок и избранного.

    Args:
        CSVResponseMixin (type): Кастомный миксин для экспорта csv-файла.
    """

    queryset = (Recipe.objects.select_related('author')
                .prefetch_related('tags', 'ingredients').all())
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filterset_class = RecipeFilterSet
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """Для SAFE_METHODS используем другой сериализатор."""
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return RecipeSerializer

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        """Загрузка списка покупок."""
        ingredient_list = (
            IngredientQuantity.objects.filter(
                recipe__shopping_list__user=request.user
            ).values(
                'ingredients__name',
                'ingredients__measurement_unit',
            ).order_by(
                'ingredients__name',
            ).annotate(sum=Sum('amount'))
        )
        filename = "shopping_list.pdf"
        return self.render_to_pdf_response(ingredient_list, filename)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        """Добавление/Удаление рецептов в списке покупок."""
        return recipe_post_delete_action(ShoppingListSerializer,
                                         Shopping, request, pk, Recipe)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def favorite(self, request, pk):
        """Добавление/Удаление рецептов в избранном."""
        return recipe_post_delete_action(FavouriteListSerializer,
                                         Favourites, request, pk, Recipe)
