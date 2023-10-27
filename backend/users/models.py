from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from obsceneLang.validators import validate_no_obscenities


class User(AbstractUser):
    """Модель для пользователей

    Params:
        Roles (class): Описание ролей
        username (CharField[str]): username пользователя
        email (EmailField[str]): email пользователя
        bio (TextField[str]): биография
        role (CharField[str]): роль, возможны user, admin
    """

    username = models.CharField(
        'Логин',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        db_index=True,
        validators=(
            validate_no_obscenities,
            UnicodeUsernameValidator(),
        )
    )
    email = models.EmailField(
        'Почтовый адрес',
        unique=True,
        max_length=settings.EMAIL_MAX_LENGTH,
        db_index=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=settings.FIRSTNAME_MAX_LENGTH,
        validators=(
            validate_no_obscenities,
        )
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LASTNAME_MAX_LENGTH,
        validators=(
            validate_no_obscenities,
        )
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username[:settings.USERNAME_MAX_LENGTH]


class Subscription(models.Model):
    """Модель для подписок

    Params:
        user (ForeignKey[User]): пользователь
        author (ForeignKey[User]): автор
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('author', )
        constraints = (
            models.UniqueConstraint(
                name='unique_relationships',
                fields=('user', 'author'),
            ),
        )

    def clean(self):
        """Валидация самоподписки."""
        if self.user == self.author:
            raise ValidationError('Подписка на самого себя, запрещена!')

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
