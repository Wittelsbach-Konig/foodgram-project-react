from django.contrib import admin

from recipes.models import (
    Recipe, Ingredient,
    IngredientQuantity, Tag,
    Favourites, Shopping,
)


class IngredientInline(admin.TabularInline):
    """Встроенный интерфейс для ингредиентов в рецептах админки."""

    model = IngredientQuantity
    extra = 2
    min_num = 1

    def has_delete_permission(self, request, obj=None):
        ingredient_count = obj.ingredients.count() if obj else 0
        if ingredient_count == 1:
            return False
        return super().has_delete_permission(request, obj)


class RecipeAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для списка рецептов. """

    list_display: tuple = (
        'pk',
        'name',
        'author',
        'get_favourites',
        'show_tags',
        'pub_date',
    )
    list_filter: tuple = (
        'author',
        'name',
        'tags',
    )
    search_fields: tuple = (
        'name',
        'author',
    )
    inlines = (IngredientInline,)

    @staticmethod
    def get_favourites(obj):
        return obj.favourites_list.count()

    get_favourites.short_description = (
        'Количество добавлений рецепта в избранное'
    )

    def show_tags(self, obj):
        return '\n'.join([tag.name for tag in obj.tags.all()])

    show_tags.short_description = (
        'Cписок тегов'
    )


class IngredientAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для списка ингредиентов. """

    list_display: tuple = (
        'pk',
        'name',
        'measurement_unit',
    )
    list_filter: tuple = (
        'name',
    )
    search_fields: tuple = (
        'name',
    )


class IngredientQuantityAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для количества ингредиентов. """

    list_display: tuple = (
        'pk',
        'recipe',
        'ingredients',
        'amount',
    )


class TagAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для тегов. """

    list_display: tuple = (
        'pk',
        'name',
        'color',
        'slug',
    )


class ListAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для списка ибранного/покупок. """

    list_display: tuple = (
        'pk',
        'user',
        'recipe'
    )
    search_fields: tuple = (
        'user',
        'recipe',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientQuantity, IngredientQuantityAdmin)
admin.site.register(Favourites, ListAdmin)
admin.site.register(Shopping, ListAdmin)
