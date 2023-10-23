from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.conf import settings

from obsceneLang.validators import validate_no_obscenities


class CustomUserManager(UserManager):
    """ Менеджер для кастомной модели User. """

    def create_superuser(self, username, email=None,
                         password=None, **extra_fields):
        """Переопределённая функция создания суперпользователя.

        Args:
            username (str): имя пользователя
            email (str, optional): почтовый адрес. Defaults to None.
            password (str, optional): пароль. Defaults to None.

        Raises:
            ValueError: is_staff должен быть равен True
            ValueError: is_superuser должен быть равен True
            ValueError: is_admin должен быть равен True

        Returns:
            _create_user(): создание пользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('role', User.Roles.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('role') != User.Roles.ADMIN:
            raise ValueError('Superuser must have is_admin=True.')

        return self._create_user(username, email, password, **extra_fields)


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
        max_length=settings.FIRSTNAME_MAX_LENGTH,
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
        max_length=settings.ROLE_MAX_LENGTH,
        choices=Roles.choices,
        default=Roles.USER,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]

    objects = CustomUserManager()

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
