import csv
import io
from django.http import HttpResponse
from rest_framework import mixins, viewsets

from core.permissions import IsAdminOrReadOnly
from core.serializers import CompactRecipeSerializer


class GetRecipe():
    """Миксин для получения списка рецептов."""

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return CompactRecipeSerializer(recipes, many=True, read_only=True).data


class GetRecipesCount():
    """Миксин для получения кол-ва рецептов."""

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class GetIsSubscribed():
    """Миксин для проверки подписки."""

    def get_is_subscribed(self, obj):
        """Отображение подписки на пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()


class GetFavorites():
    """Миксин для проверки списка избранного."""

    def get_is_favorited(self, obj):
        """Находится ли в избранном."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favourites_list.filter(recipe=obj.id).exists()


class GetShoppingList():
    """Миксин для проверки списка покупок."""

    def get_is_in_shopping_cart(self, obj):
        """Находится ли в списке покупок."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_list.filter(recipe=obj.id).exists()


class ListAndRetrieveModelMixin(viewsets.GenericViewSet,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,):
    """
    Кастомный, абстрактный миксин.
    Доступные запросы: GET.
    Доступен всем пользователям.
    """

    permisson_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class CSVResponseMixin():
    """Миксин для преобразования данных в csv."""

    def get_csv_header(self, data):
        """Определить названия столбцов."""
        if data and len(data) > 0:
            return data[0].keys()
        return []

    def render_to_csv_response(self, data, filename):
        """Записать данные в csv и отправить через HttpResponse."""
        if not data:
            return HttpResponse(content_type='text/csv')
        header = self.get_csv_header(data)
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=header, delimiter=';')
        writer.writeheader()

        for row in data:
            writer.writerow(row)
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        response.write(output.getvalue())

        return response
