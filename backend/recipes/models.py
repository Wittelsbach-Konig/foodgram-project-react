from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from colorfield.fields import ColorField


class Tag(models.Model):
    """Модель для тега.

    Params:
        name (CharField[str]): название тега
        color (): цветовой код
        slug (): slug
    """

    name = models.CharField(
        'Название тега',
        unique=True,
        max_length=settings.TAGNAME_MAX_LENGTH,
        db_index=True
    )
    color = ColorField(
        default='#8420D3',
        max_length=settings.COLOR_CODE_MAX_LENGTH,
        verbose_name='Цветовой код',
        unique=True,
    )
    slug = models.SlugField(
        'Уникальный фрагмент URL',
        unique=True,
        max_length=settings.SLUG_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    """Модель для ингредиентов.

    Params:
        name (CharField[str]): название ингредиента
        measurement_unit (CharField[str]): единица измерения
    """

    name = models.CharField(
        'Название ингредиента',
        max_length=settings.INGREDIENT_NAME_MAX_LENGTH,
        db_index=True,
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=settings.MEASUREMENT_UNIT_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                name='unique_ingredient',
                fields=('name', 'measurement_unit'),
            ),
        )

    def __str__(self) -> str:
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    """Модель для рецептов.

    Params:
        author (ForeignKey[User]): автор рецепта
        name (CharField[User]): название рецепта
        image (ImageField): картинка рецепта
        text (TextField[str]): текстовое описание
        ingredients (ForeignKey[IngredientQuantity]): продукты для рецепту
        tags (ForeignKey[Tag]): тег
        cooking_time (PositiveSmallIntegerField[int]): время приготовления
        pub_date (DateTimeField[datetime]): время публикации
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=settings.RECIPE_NAME_MAX_LENGTH,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientQuantity',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления в минутах',
        validators=(
            MinValueValidator(
                settings.MIN_VALUE,
                (f'Время приготовления не может '
                 f'быть меньше {settings.MIN_VALUE}')
            ),
            MaxValueValidator(
                settings.MAX_VALUE,
                f'Максимальное кол-во равно {settings.MAX_VALUE}',
            )
        )
    )
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientQuantity(models.Model):
    """Модель для связи ингредиентов и рецептов.

    Params:
        recipe (ForeignKey[Recipe]): рецепт
        ingredient (ForeignKey[Ingredient]): ингредиент
        amount (PositiveSmallIntegerField[int]): кол-во
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_quantity',
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_quantity',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                settings.MIN_VALUE,
                f'Минимальное кол-во равно {settings.MIN_VALUE}'
            ),
            MaxValueValidator(
                settings.MAX_VALUE,
                f'Максимальное кол-во равно {settings.MAX_VALUE}',
            )
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                name='unique_ingredients',
                fields=('recipe', 'ingredients'),
            ),
        )

    def __str__(self) -> str:
        return f"{self.recipe}: {self.amount} {self.ingredients}"


class AbstractRecipeListModel(models.Model):
    """Абстрактная модель для списка рецептов - Избранного/Покупок.

    Params:
        user (ForeignKey[User]): пользователь
        recipe (ForeignKey[Recipe]): рецепт
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='%(class)s_list',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='%(class)s_list',
    )

    class Meta:
        abstract = True
        constraints = (
            models.UniqueConstraint(
                name='unique_shopping',
                fields=('user', 'recipe')
            ),
        )


class Shopping(AbstractRecipeListModel):
    """Модель для списка покупок.

    Args:
        AbstractRecipeListModel (Model): абстрактная модель
    """

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self) -> str:
        return f"{self.user} добавил рецепт {self.recipe} в список покупок"


class Favourites(AbstractRecipeListModel):
    """Модель для Избранного списка рецептов.

    Args:
        AbstractRecipeListModel (Model): абстрактная модель
    """

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self) -> str:
        return f"{self.user} добавил рецепт {self.recipe} в избранное"
