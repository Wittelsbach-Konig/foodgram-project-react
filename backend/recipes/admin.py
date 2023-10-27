from django.contrib import admin

from .models import (
    Recipe, Ingredient,
    IngredientQuantity, Tag,
    Favourites, Shopping,
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
        return obj.favourites_list.count()

    def show_tags(self, obj):
        return '\n'.join([tag.name for tag in obj.tags.all()])


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
