import io
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import styles
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework import mixins, viewsets

from core.permissions import IsAdminOrReadOnly
from core.serializers import CompactRecipeSerializer


class GetRecipe:
    """Миксин для получения списка рецептов."""

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.query_params.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        return CompactRecipeSerializer(recipes, many=True, read_only=True).data


class GetRecipesCount:
    """Миксин для получения кол-ва рецептов."""

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class GetIsSubscribed:
    """Миксин для проверки подписки."""

    def get_is_subscribed(self, obj):
        """Отображение подписки на пользователя."""
        user = self.context.get('request').user
        return (not user.is_anonymous
                and user.follower.filter(author=obj.id).exists())


class GetFavorites:
    """Миксин для проверки списка избранного."""

    def get_is_favorited(self, obj):
        """Находится ли в избранном."""
        user = self.context.get('request').user
        return (not user.is_anonymous
                and user.favourites_list.filter(recipe=obj.id).exists())


class GetShoppingList:
    """Миксин для проверки списка покупок."""

    def get_is_in_shopping_cart(self, obj):
        """Находится ли в списке покупок."""
        user = self.context.get('request').user
        return (not user.is_anonymous
                and user.shopping_list.filter(recipe=obj.id).exists())


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


class PDFResponseMixin:
    """Миксин для преобразования данных в PDF."""

    def render_to_pdf_response(self, ingredients, filename):
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer, pagesize=letter)

        elements = []

        pdfmetrics.registerFont(
            TTFont("TimesNewRoman", "static/data/TimesNewRomanRegular.ttf")
        )
        title_style = styles.getSampleStyleSheet()["Title"]
        title_style.alignment = 1
        title_style.fontName = "TimesNewRoman"
        elements.append(Paragraph("Ингредиенты", title_style))

        normal_style = styles.getSampleStyleSheet()["Normal"]
        normal_style.fontName = "TimesNewRoman"

        for ingredient in ingredients:
            name = ingredient["ingredients__name"]
            measurement_unit = ingredient["ingredients__measurement_unit"]
            amount = ingredient["sum"]
            ingredient_text = f"{name} - {amount} ({measurement_unit})"
            elements.append(Paragraph(ingredient_text, normal_style))

        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response.write(buffer.read())

        return response
