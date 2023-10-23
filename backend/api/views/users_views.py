from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as BaseUserViewSet
from rest_framework import permissions, status
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
from core.utils import get_object_or_400


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
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            if Subscription.objects.filter(user=user,
                                           author=author).exists():
                return Response(
                    {"error": "Запись уже существует."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            data = {
                'user': user.pk,
                'author': author.pk,
            }
            serializer = SubscribtionCheckSerializer(
                data=data,
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = SubscribtionSerializer(author,
                                                context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if not Subscription.objects.filter(user=user,
                                           author=author).exists():
            return Response(
                {"error": "Запись уже удалена."},
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = get_object_or_404(
            Subscription,
            user=user,
            author=author,
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
