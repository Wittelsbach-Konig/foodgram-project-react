from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from core.serializers import CompactRecipeSerializer


def get_object_or_400(model, **kwargs):
    """Возвращает объект или HTTP_400_Bad_Request."""
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        raise ValidationError("Объект не найден", code="object_not_found")


def recipe_post_delete_action(custom_serializer, model, request, pk, db_model):
    """
    Абстрактный action для POST/DELETE методов.
    Для shopping_cart/favourite.
    """
    user = request.user
    if request.method == 'POST':
        return recipe_post_action(custom_serializer, model, user, pk, db_model)
    return recipe_delete_action(model, user, pk, db_model)


def recipe_post_action(custom_serializer, model, user, pk, db_model):
    """Абстрактный action для POST метода для shopping_cart/favourite."""
    recipe = get_object_or_400(db_model, id=pk)
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


def recipe_delete_action(model, user, pk, db_model):
    """Абстрактный action для DELETE метода для shopping_cart/favourite."""
    recipe = get_object_or_404(db_model, id=pk)
    if model.objects.filter(user=user, recipe=recipe).exists():
        model_recipe = get_object_or_404(model,
                                         user=user,
                                         recipe=recipe)
        model_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Запись уже удалена."},
                    status=status.HTTP_400_BAD_REQUEST)


def user_post_delete_action(request, id, model, custom_serializer,
                            db_model, check_serializer):
    """Абстрактный action для POST/DELETE методов для subscribe."""
    user = request.user
    author = get_object_or_404(db_model, pk=id)
    if request.method == 'POST':
        return user_post_action(request, user, author, model,
                                custom_serializer, check_serializer)
    return user_delete_action(user, author, model)


def user_post_action(request, user, author, model,
                     custom_serializer, check_serializer):
    """Абстрактный action для POST метода для subscribe."""
    if not model.objects.filter(user=user,
                                author=author).exists():
        data = {'user': user.pk, 'author': author.pk}
        serializer = check_serializer(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = custom_serializer(author, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"error": "Запись уже существует."},
                    status=status.HTTP_400_BAD_REQUEST)


def user_delete_action(user, author, model):
    """Абстрактный action для DELETE метода для subscribe."""
    if model.objects.filter(user=user,
                            author=author).exists():
        subscription = get_object_or_404(model,
                                         user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"error": "Запись уже удалена."},
                    status=status.HTTP_400_BAD_REQUEST)
