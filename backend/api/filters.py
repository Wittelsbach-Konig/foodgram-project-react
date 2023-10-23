from django_filters.rest_framework import (
    CharFilter,
    FilterSet,
    filters,
)
from django_filters import ModelMultipleChoiceFilter

from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
)
from users.models import User


class IngredientFilterSet(FilterSet):
    """Фильтр сет для ингредиентов, поиск по названию."""

    name = CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    """Фильтр сет для рецептов, отображение избранного и списка покупок."""

    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_is_shopping_cart")

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(
                favourites_list__user__id=self.request.user.id
            )
        return queryset

    def get_is_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(
                shopping_list__user__id=self.request.user.id
            )
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )
