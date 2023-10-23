from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from api.serializers.compact_recipe_serializers import (
    CompactRecipeSerializer,
)
from recipes.models import Recipe


def get_object_or_400(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise ValidationError("Объект не найден", code="object_not_found")


def abstract_post_delete_action(custom_serializer,
                                model, request, pk):
    """Абстрактный action для POST/DELETE методов."""
    user = request.user
    if request.method == 'POST':
        return abstract_post_action(custom_serializer,
                                    model, user, pk)
    return abstract_delete_action(model, user, pk)


def abstract_post_action(custom_serializer,
                         model, user, pk):
    """Абстрактный action для POST метода."""
    recipe = get_object_or_400(Recipe, id=pk)
    if not model.objects.filter(user=user, recipe=recipe).exists():
        data = {'user': user.id, 'recipe': recipe.id}
        serializer = custom_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        compact_recipe_serializer = CompactRecipeSerializer(recipe)
        return Response(compact_recipe_serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response({"error": "Запись уже существует."},
                    status=status.HTTP_400_BAD_REQUEST)


def abstract_delete_action(model, user, pk):
    """Абстрактный action для DELETE метода."""
    recipe = get_object_or_404(Recipe, id=pk)
    if model.objects.filter(user=user, recipe=recipe).exists():
        model_recipe = get_object_or_404(model,
                                         user=user,
                                         recipe=recipe)
        model_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Запись уже удалена."},
                    status=status.HTTP_400_BAD_REQUEST)
