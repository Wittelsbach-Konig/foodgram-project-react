from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import (
    User,
    Subscription,
)
from api.serializers.users_serializers import (
    UserSerializer,
    SubscribtionSerializer,
    SubscribtionCheckSerializer,
)
from core.pagination import CustomPagination
from core.utils import user_post_delete_action


class UserViewSet(BaseUserViewSet):
    """ViewSet для Пользователей."""

    query = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=('get', ),
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
        url_name='me',
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
        url_path='subscribe',
        url_name='subscribe',
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
        url_path='subscriptions',
        url_name='subscriptions',
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
