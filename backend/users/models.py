from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
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

    class Roles(models.TextChoices):
        """Возможные роли пользователей

        Literals:
            USER (str): Роль пользователя
            ADMIN (str): Роль администратора
        """
        USER = 'user', 'Пользователь'
        ADMIN = 'admin', 'Администратор'

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
        max_length=settings.NAME_MAX_LENGTH,
        blank=True,
        validators=(
            validate_no_obscenities,
        )
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=settings.LASTNAME_MAX_LENGTH,
        blank=True,
        validators=(
            validate_no_obscenities,
        )
    )
    role = models.CharField(
        'Роль',
        choices=Roles.choices,
        default=Roles.USER,
    )

    REQUIRED_FIELDS = [
        'email',
    ]

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self) -> bool:
        """Проверка является ли пользователь админом."""
        return self.is_superuser or self.role == self.Roles.ADMIN.value

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
        get_latest_by = ('author')
        constraints = (
            models.UniqueConstraint(
                name='unique_relationships',
                fields=('user', 'author'),
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
