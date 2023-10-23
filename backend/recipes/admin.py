from django.contrib import admin

from .models import (
    Recipe, Ingredient,
    IngredientQuantity, Tag,
    FavouriteList, ShoppingList,
)


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

    def get_favourites(self, obj):
        return obj.favourites_recipe.count()

    def show_tags(self, obj):
        return '\n'.join([tag.tag_name for tag in obj.recipe_tags.all()])


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


class ShoppingListAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для списка покупок. """

    list_display: tuple = (
        'pk',
        'user',
        'recipe'
    )
    search_fields: tuple = (
        'user',
        'recipe',
    )


class FavouritesAdmin(admin.ModelAdmin):
    """ Интерфейс администратора для избранного списка. """

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
admin.site.register(FavouriteList, FavouritesAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
