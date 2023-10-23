from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.serializers.compact_recipe_serializers import (
    CompactRecipeSerializer,
)
from recipes.models import Recipe


def abstract_post_delete_action(custom_serializer,
                                model, request, pk):
    """Абстрактный action для POST, DELETE методов."""
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'POST':
        serializer = custom_serializer(
            data={
                'user': request.user.id,
                'recipe': recipe.id,
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
        user=request.user,
        recipe=recipe,
    )
    model_recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
