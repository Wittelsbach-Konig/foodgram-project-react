from django.contrib.auth.validators import UnicodeUsernameValidator
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer

from users.models import (
    User,
    Subscription,
)
from obsceneLang.validators import validate_no_obscenities
from core.mixins import (
    GetIsSubscribed,
    GetRecipe,
    GetRecipesCount,
)


class UserSerializer(serializers.ModelSerializer,
                     GetIsSubscribed):
    """Сериалайзер для пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_subscribed',
        )


class UserSignUpSerializer(UserCreateSerializer):
    """Сериалайзер для регистрации."""

    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(validate_no_obscenities,
                    UnicodeUsernameValidator(),)
    )
    first_name = serializers.CharField(
        max_length=settings.FIRSTNAME_MAX_LENGTH,
        validators=(validate_no_obscenities,)
    )
    last_name = serializers.CharField(
        max_length=settings.LASTNAME_MAX_LENGTH,
        validators=(validate_no_obscenities,)
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}


class SubscribtionSerializer(UserSerializer,
                             GetRecipe,
                             GetRecipesCount):
    """Сериалайзер для отображения Подписок."""

    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )


class SubscribtionCheckSerializer(serializers.ModelSerializer):
    """Сериалайзер для проверки Подписок."""

    class Meta:
        model = Subscription
        fields = (
            'user',
            'author',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=(Subscription.objects
                          .select_related('user', 'author')
                          .all()),
                fields=('user', 'author'),
            )
        ]

    def validate(self, data):
        """Валидация самоподписки."""
        if self.context.get('request').user == data.get('author'):
            raise serializers.ValidationError(
                'Нельзя подписываться на себя!'
            )
        return data
