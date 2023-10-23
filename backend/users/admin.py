from django.contrib import admin

from .models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    """ Модель администратора для User. """

    list_display: tuple = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
    )
    list_filter: tuple = (
        'username',
        'email',
    )
    empty_value_display: str = '-пусто-'
    search_fields: tuple = (
        'username',
        'email',
    )


class SubscriptionAdmin(admin.ModelAdmin):
    """ Модель администратора для Subcription. """

    list_display: tuple = (
        'pk',
        'user',
        'author',
    )
    search_fields: tuple = (
        'user',
    )
    list_filter: tuple = (
        'user',
        'author',
    )


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
