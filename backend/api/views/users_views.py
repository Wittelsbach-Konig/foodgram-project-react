from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers.users_serializers import (SubscribtionCheckSerializer,
                                               SubscribtionSerializer,
                                               UserSerializer)
from core.pagination import CustomPagination
from core.utils import user_post_delete_action
from users.models import Subscription, User


class UserViewSet(BaseUserViewSet):
    """ViewSet для Пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        """Переопределение метода create для разрешения регистрации."""
        if not request.user.is_anonymous:
            return Response("Вы уже зарегистрированы!",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user_id = kwargs.get('id')
        if user_id and User.objects.filter(id=user_id).exists():
            return Response("Пользователь с таким id уже существует!",
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Ограничение на PUT."""
        return Response("Метод запрещён партией!",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        """Ограничение на PATCH."""
        return Response("Метод запрещён партией!",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """Ограничение на DESTROY."""
        return Response("Метод запрещён партией!",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=('get', ),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request):
        """Возврат профиля пользователя."""
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, id):
        """Создание/удаление подписок."""
        return user_post_delete_action(
            request, id, Subscription, SubscribtionSerializer,
            User, SubscribtionCheckSerializer
        )

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscriptions(self, request):
        """Получение списка подписок."""
        queryset = User.objects.filter(author__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribtionSerializer(
            pages,
            context={'request': request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)
