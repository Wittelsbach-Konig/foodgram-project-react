from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from colorfield.fields import ColorField
from users.models import User


class Tag(models.Model):
    """Модель для тега.

    Params:
        tag_name (CharField[str]): название тега
        color_code (): цветовой код
        slug (): slug
    """

    tag_name = models.CharField(
        'Название тега',
        unique=True,
        max_length=settings.NAME_MAX_LENGTH,
        db_index=True
    )
    color_code = ColorField(
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
        ordering = ('tag_name',)

    def __str__(self) -> str:
        return self.slug


class Ingredient(models.Model):
    """Модель для ингредиентов.

    Params:
        ingredient_name (CharField[str]): название ингредиента
        measurment (CharField[str]): единица измерения
    """

    ingredient_name = models.CharField(
        'Название ингредиента',
        max_length=settings.NAME_MAX_LENGTH,
        db_index=True,
    )
    measurment = models.CharField(
        'Единица измерения',
        max_length=settings.NAME_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('ingredient_name',)

    def __str__(self) -> str:
        return f"{self.ingredient_name}, {self.measurment}"


class Recipe(models.Model):
    """Модель для рецептов.

    Params:
        author (ForeignKey[User]): автор рецепта
        recipe_name (CharField[User]): название рецепта
        picture (ImageField): картинка рецепта
        text (TextField[str]): текстовое описание
        ingredients (ForeignKey[IngredientQuantity]): продукты для рецепту
        tag (ForeignKey[Tag]): тег
        cooking_time (PositiveSmallIntegerField[int]): время приготовления
        pub_date (DateTimeField[datetime]): время публикации
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    recipe_name = models.CharField(
        'Название рецепта',
        max_length=settings.NAME_MAX_LENGTH,
    )
    picture = models.ImageField(
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
    tag = models.ManyToManyField(
        Tag,
        through='TagsRecipes',
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
        return self.recipe_name


class IngredientQuantity(models.Model):
    """Модель для связи Ингредиентов и рецептов.

    Params:
        recipe (ForeignKey[Recipe]): рецепт
        ingredient (ForeignKey[Ingredient]): ингредиент
        amount (PositiveSmallIntegerField[int]): кол-во
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='in_recipe',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=(
            MinValueValidator(
                settings.MIN_VALUE,
                f'Минимальное кол-во равно {settings.MIN_VALUE}'
            ),
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                name='unique_ingredients',
                fields=('recipe', 'ingredient'),
            ),
        )

    def __str__(self) -> str:
        return f"{self.recipe}: {self.amount} {self.ingredient}"


class TagsRecipes(models.Model):
    """Модель для связи тегов и рецептов.

    Params:
        tag (ForeignKey[Tag]): тег
        recipe (ForeignKey[Recipe]): рецепт
    """

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tags_in_recipe',
        verbose_name='Теги',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список тегов'
        verbose_name_plural = 'Список тегов'
        constraints = (
            models.UniqueConstraint(
                name='unique_tag_recipe',
                fields=('tag', 'recipe'),
            ),
        )

    def __str__(self) -> str:
        return f"{self.recipe} имеет тег {self.tag}"


class ShoppingList(models.Model):
    """Модель для списка покупок.

    Params:
        user (ForeignKey[User]): пользователь
        recipe (ForeignKey[Recipe]): рецепт
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_recipe',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                name='unique_shopping',
                fields=('user', 'recipe')
            ),
        )

    def __str__(self) -> str:
        return f"{self.user} добавил рецепт {self.recipe} в список покупок"


class FavouriteList(models.Model):
    """Модель для Избранного списка рецептов.

    Params:
        user (ForeignKey[User]): пользователь
        recipe (ForeignKey[Recipe]): рецепт
    """

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favourites_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favourites_recipe',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                name='unique_favourites',
                fields=('user', 'recipe')
            ),
        )

    def __str__(self) -> str:
        return f"{self.user} добавил рецепт {self.recipe} в избранное"
